#!/usr/bin/env python3
"""
Convert face image CSV files to jsPsych stimuli.json format.

Usage:
    python convert_stimuli.py --western english_sample.csv --chinese chinese_sample.csv --output stimuli.json --image_base_url "images/"

This script:
1. Reads the CSV files with image paths
2. Extracts just the filename (you'll need to copy images to an accessible location)
3. Creates a stimuli.json file for the jsPsych experiment
4. Optionally marks some stimuli as practice trials
"""

import pandas as pd
import json
import argparse
import os
from pathlib import Path

def extract_filename(path):
    """Extract just the filename from a full path."""
    return os.path.basename(path)

def convert_to_stimuli(western_csv, chinese_csv, output_path, image_base_url="images/", 
                       n_practice_per_group=3, sample_n=None):
    """
    Convert CSV files to jsPsych stimuli format.
    
    Parameters:
    -----------
    western_csv : str
        Path to CSV with Western (Google) images
    chinese_csv : str
        Path to CSV with Chinese (Baidu) images  
    output_path : str
        Path for output JSON file
    image_base_url : str
        Base URL/path where images will be hosted (e.g., "images/" or "https://yourserver.com/images/")
    n_practice_per_group : int
        Number of practice trials per source category
    sample_n : int or None
        If specified, randomly sample this many images per group (useful for testing)
    """
    
    # Read CSVs
    western_df = pd.read_csv(western_csv)
    chinese_df = pd.read_csv(chinese_csv)
    
    print(f"Loaded {len(western_df)} Western images and {len(chinese_df)} Chinese images")
    
    # Sample if requested
    if sample_n:
        western_df = western_df.sample(min(sample_n, len(western_df)), random_state=42)
        chinese_df = chinese_df.sample(min(sample_n, len(chinese_df)), random_state=42)
        print(f"Sampled to {len(western_df)} Western and {len(chinese_df)} Chinese images")
    
    stimuli = []
    
    # Process Western images
    for idx, row in western_df.iterrows():
        filename = extract_filename(row['image_path'])
        is_practice = idx < n_practice_per_group
        
        stimuli.append({
            "image": image_base_url + "western/" + filename,
            "source": "western",
            "image_id": filename,
            "is_practice": is_practice,
            "original_path": row['image_path'],
            # Include useful metadata
            "race": row.get('top_race_4', ''),
            "gender": row.get('top_gender', ''),
            "age": row.get('top_age', '')
        })
    
    # Process Chinese images
    for idx, row in chinese_df.iterrows():
        filename = extract_filename(row['image_path'])
        is_practice = idx < n_practice_per_group
        
        stimuli.append({
            "image": image_base_url + "chinese/" + filename,
            "source": "chinese",
            "image_id": filename,
            "is_practice": is_practice,
            "original_path": row['image_path'],
            # Include useful metadata
            "race": row.get('top_race_4', ''),
            "gender": row.get('top_gender', ''),
            "age": row.get('top_age', '')
        })
    
    # Create output structure
    output = {
        "experiment_info": {
            "total_stimuli": len(stimuli),
            "practice_trials": n_practice_per_group * 2,
            "main_trials": len(stimuli) - (n_practice_per_group * 2),
            "western_count": len(western_df),
            "chinese_count": len(chinese_df)
        },
        "stimuli": stimuli
    }
    
    # Write JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nCreated {output_path}")
    print(f"  Total stimuli: {len(stimuli)}")
    print(f"  Practice trials: {n_practice_per_group * 2}")
    print(f"  Main trials: {len(stimuli) - (n_practice_per_group * 2)}")
    
    # Print image copy instructions
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print(f"\n1. Create image folders in your experiment directory:")
    print(f"   mkdir -p images/western images/chinese")
    print(f"\n2. Copy images to the appropriate folders:")
    print(f"   - Western images → images/western/")
    print(f"   - Chinese images → images/chinese/")
    print(f"\n3. If hosting elsewhere, update image_base_url in stimuli.json")
    print("="*60)
    
    return output

def main():
    parser = argparse.ArgumentParser(description='Convert CSV files to jsPsych stimuli format')
    parser.add_argument('--western', required=True, help='Path to Western/Google images CSV')
    parser.add_argument('--chinese', required=True, help='Path to Chinese/Baidu images CSV')
    parser.add_argument('--output', default='stimuli.json', help='Output JSON path')
    parser.add_argument('--image_base_url', default='images/', help='Base URL for images')
    parser.add_argument('--n_practice', type=int, default=3, help='Practice trials per group')
    parser.add_argument('--sample', type=int, default=None, help='Sample N images per group (for testing)')
    
    args = parser.parse_args()
    
    convert_to_stimuli(
        args.western, 
        args.chinese, 
        args.output,
        args.image_base_url,
        args.n_practice,
        args.sample
    )

if __name__ == '__main__':
    main()
