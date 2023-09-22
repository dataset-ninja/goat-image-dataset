# https://data.mendeley.com/datasets/4skwhnrscr/2

import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def recursive_listdir(path):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            yield from recursive_listdir(full_path)
        else:
            yield full_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Goat Image"
    dataset1_path = "/mnt/d/datasetninja-raw/goat-image-dataset/4skwhnrscr-2/upload"
    dataset2_path = "/mnt/d/datasetninja-raw/goat-image-dataset/4skwhnrscr-2/1selected"
    batch_size = 30
    ds_names = ["dataset_1", "dataset_2"]
    images_ext = ".jpg"
    bboxes_ext = ".txt"

    def create_ann(image_path):
        labels = []
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        if ds_name == "dataset_2":
            tag_name = int(image_path.split("/")[-2])
            tags = [sly.Tag(tag_meta, value=tag_name) for tag_meta in tag_metas]

            return sly.Annotation(img_size=(img_height, img_wight), img_tags=tags)

        ann_path = os.path.join(dataset1_path, get_file_name(image_path) + bboxes_ext)

        with open(ann_path) as f:
            content = f.read().split("\n")

        for curr_data in content:
            if len(curr_data) != 0:
                ann_data = list(map(float, curr_data.rstrip().split(" ")))
                curr_obj_class = idx_to_obj_class[int(ann_data[0])]
                left = int((ann_data[1] - ann_data[3] / 2) * img_wight)
                right = int((ann_data[1] + ann_data[3] / 2) * img_wight)
                top = int((ann_data[2] - ann_data[4] / 2) * img_height)
                bottom = int((ann_data[2] + ann_data[4] / 2) * img_height)
                rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                label = sly.Label(rectangle, curr_obj_class)
                labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    idx_to_obj_class = {
        0: sly.ObjClass("face", sly.Rectangle),
        1: sly.ObjClass("eye", sly.Rectangle),
        2: sly.ObjClass("mouth", sly.Rectangle),
        3: sly.ObjClass("ear", sly.Rectangle),
    }

    tag_metas = [sly.TagMeta("goat_id", sly.TagValueType.ANY_NUMBER)]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(idx_to_obj_class.values()), tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, dataset_path in zip(ds_names, [dataset1_path, dataset2_path]):
        images_pathes = [
            item for item in recursive_listdir(dataset_path) if get_file_ext(item) == images_ext
        ]

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            images_names_batch = [os.path.basename(path) for path in img_pathes_batch]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))
    return project
