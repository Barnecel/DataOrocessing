import argparse
import json
import pickle


def prepare_annotations(annotations_per_image, images_info, net_input_size):
    """Prepare labels for training. For each annotated person calculates center
    to perform crop around it during the training. Also converts data to the internal format.

    :param annotations_per_image: all annotations for specified image id
    :param images_info: auxiliary information about all images
    :param net_input_size: network input size during training
    :return: list of prepared annotations
    """
    prepared_annotations = []
    for _, annotations in annotations_per_image.items():
        previous_centers = []
        for annotation in annotations[0]:
            if (annotation['num_keypoints'] < 4
                    or annotation['area'] < 32 * 32):
                continue
            person_center = [annotation['bbox'][0] + annotation['bbox'][2] / 2,
                             annotation['bbox'][1] + annotation['bbox'][3] / 2]
            is_close = False
            for previous_center in previous_centers:
                distance_to_previous = ((person_center[0] - previous_center[0]) ** 2
                                        + (person_center[1] - previous_center[1]) ** 2) ** 0.5
                if distance_to_previous < min(previous_center[2], previous_center[3], annotation['bbox'][2], annotation['bbox'][3]) * 0.3:
                    is_close = True
                    break
            if is_close:
                continue

            prepared_annotation = {
                'img_paths': images_info[annotation['image_id']]['file_name'],
                'img_width': images_info[annotation['image_id']]['width'],
                'img_height': images_info[annotation['image_id']]['height'],
                'objpos': person_center, # 人体的中心点
                'image_id': annotation['image_id'],
                'bbox': annotation['bbox'],
                'segment_area': annotation['area'],
                'scale_provided': max(annotation['bbox'][2], annotation['bbox'][3]) / net_input_size, # 人体的高占网络的大小
                'num_keypoints': annotation['num_keypoints'],
                'segmentations': annotations[1] # 存放拥挤的mask
            }

            keypoints = []
            for i in range(len(annotation['keypoints']) // 3):
                keypoint = [annotation['keypoints'][i * 3], annotation['keypoints'][i * 3 + 1], 2]
                if annotation['keypoints'][i * 3 + 2] == 1:
                    keypoint[2] = 0
                elif annotation['keypoints'][i * 3 + 2] == 2:
                    keypoint[2] = 1
                keypoints.append(keypoint)
            prepared_annotation['keypoints'] = keypoints

            prepared_other_annotations = []
            for other_annotation in annotations[0]:
                if other_annotation == annotation:
                    continue

                prepared_other_annotation = {
                    'objpos': [other_annotation['bbox'][0] + other_annotation['bbox'][2] / 2,
                               other_annotation['bbox'][1] + other_annotation['bbox'][3] / 2],
                    'bbox': other_annotation['bbox'],
                    'segment_area': other_annotation['area'],
                    'scale_provided': other_annotation['bbox'][3] / net_input_size,
                    'num_keypoints': other_annotation['num_keypoints']
                }

                keypoints = []
                for i in range(len(other_annotation['keypoints']) // 3):
                    keypoint = [other_annotation['keypoints'][i * 3], other_annotation['keypoints'][i * 3 + 1], 2]
                    if other_annotation['keypoints'][i * 3 + 2] == 1:
                        keypoint[2] = 0
                    elif other_annotation['keypoints'][i * 3 + 2] == 2:
                        keypoint[2] = 1
                    keypoints.append(keypoint)
                prepared_other_annotation['keypoints'] = keypoints
                prepared_other_annotations.append(prepared_other_annotation)

            prepared_annotation['processed_other_annotations'] = prepared_other_annotations
            prepared_annotations.append(prepared_annotation)

            previous_centers.append((person_center[0], person_center[1], annotation['bbox'][2], annotation['bbox'][3]))
    return prepared_annotations


if __name__ == '__main__':
    label_file = '/home/p/COCO/annotations/person_keypoints_train2017.json'
    # label_file = '/home/p/data/COCO/annotations_14_17/person_keypoints_val2014.json'
    label_file = '/home/p/data/COCO/annotations_14_17/person_keypoints_train2017.json'

    outName = 'prepared_train_home02.pkl'

    parser = argparse.ArgumentParser()
    parser.add_argument('--labels', type=str, default=label_file, help='path to json with keypoints train labels')
    parser.add_argument('--output-name', type=str, default=outName,
                        help='name of output file with prepared keypoints annotation')
    parser.add_argument('--net-input-size', type=int, default=480, help='network input size')
    args = parser.parse_args()
    with open(args.labels, 'r') as f:
        data = json.load(f)

    annotations_per_image_mapping = {}
    for annotation in data['annotations']:
        if annotation['num_keypoints'] != 0 and not annotation['iscrowd']:
            if annotation['image_id'] not in annotations_per_image_mapping:
                annotations_per_image_mapping[annotation['image_id']] = [[], []]
            annotations_per_image_mapping[annotation['image_id']][0].append(annotation)

    crowd_segmentations_per_image_mapping = {}
    for annotation in data['annotations']:
        if annotation['iscrowd']:
            if annotation['image_id'] not in crowd_segmentations_per_image_mapping:
                crowd_segmentations_per_image_mapping[annotation['image_id']] = []
            crowd_segmentations_per_image_mapping[annotation['image_id']].append(annotation['segmentation'])

    for image_id, crowd_segmentations in crowd_segmentations_per_image_mapping.items():
        if image_id in annotations_per_image_mapping:
            annotations_per_image_mapping[image_id][1] = crowd_segmentations

    images_info = {}
    for image_info in data['images']:
        images_info[image_info['id']] = image_info

    prepared_annotations = prepare_annotations(annotations_per_image_mapping, images_info, args.net_input_size)

    with open(args.output_name, 'wb') as f:
        pickle.dump(prepared_annotations, f)


'''
<class 'list'>: 
[
    [
        {
        'segmentation': [
            [267.03, 243.78, 314.59, 154.05, 357.84, 136.76, 374.05, 104.32, 410.81, 110.81, 429.19, 131.35, 420.54, 165.95, 451.89, 209.19, 464.86, 240.54, 480, 253.51, 484.32, 263.24, 496.22, 271.89, 484.32, 278.38, 438.92, 257.84, 401.08, 216.76, 370.81, 247.03, 414.05, 277.3, 433.51, 304.32, 443.24, 323.78, 400, 362.7, 376.22, 375.68, 400, 418.92, 394.59, 424.32, 337.3, 382.16, 337.3, 371.35, 388.11, 327.03, 341.62, 301.08, 311.35, 276.22, 304.86, 263.24, 294.05, 249.19]
            ], 
        'num_keypoints': 8, 
        'area': 28292.08625, 
        'iscrowd': 0, 
        'keypoints': 
        [0, 0, 0, 0, 0,   0,   0, 0,   0,   0, 0,   0,   0, 0, 0, 325, 160, 2,   398, 177, 2, 0, 0,   0, 437, 238, 
         2, 0, 0, 0, 477, 270, 2, 287, 255, 1, 339, 267, 2, 0, 0, 0,   423, 314, 2,   0,   0, 0, 355, 367, 2],
         'image_id': 537548, 
         'bbox': [267.03, 104.32, 229.19, 320], 
         'category_id': 1, 
         'id': 183020}], []]
'''
