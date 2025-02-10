import os
import argparse
import pandas as pd

#############################

def get_triplet(frame_annotations):
    triplet = [annotation[0] for annotation in frame_annotations]
    return triplet

def extract_triplet_annotations(df):
    #take only the annotations column
    annotations = df[['annotations']].rename_axis('frame_id')

    #drop non-annotation rows
    annotations = annotations[annotations['annotations'].notnull()]

    #extract triplet labels from entire label
    annotations['triplets'] = [get_triplet(row) for row in annotations['annotations']]

    #remove label list column
    annotations.drop(columns=['annotations'], inplace=True)
    
    #sort by frame num
    annotations.index = annotations.index.astype('int64')
    annotations = annotations.sort_index()
    
    return annotations

def process_file(filename, foldername, save_path):
    video = filename[:-5]
    video_id = video[3:]
    print(video)
    csv_name = video+'.csv'

    df = pd.read_json(foldername+filename)

    annotations = extract_triplet_annotations(df)
    
    #add column for video_id
    annotations.insert(0, 'video_id', video_id)

    annotations.to_csv(save_path+csv_name)
    
def process_folder(folderpath, save_path):
    folder_path = os.fsencode(folderpath)
    
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            process_file(filename, folderpath, save_path)
            continue
        else:
            continue
    
#############################

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract CSV of framewise triplets from Cholectriplet format JSON")
    parser.add_argument("--json", required=True, type=str)
    parser.add_argument("--save", required=True, type=str)
    args = parser.parse_args()

    json_path = args.json
    save_path = args.save

    process_folder(json_path, save_path)
