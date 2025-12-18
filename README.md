# Cultural Face Classification Task

A jsPsych 7.3 experiment for 2AFC classification of face images by cultural source (Western/Google vs Chinese/Baidu).

## Quick Setup for Cognition.run

### 1. Prepare your images

Create the folder structure:
```
your-repo/
├── experiment.html
├── stimuli.json
├── convert_stimuli.py
├── README.md
└── images/
    ├── western/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── chinese/
        ├── image1.jpg
        ├── image2.jpg
        └── ...
```

Copy your images into the appropriate folders. The filenames should match those in `stimuli.json`.

### 2. Update stimuli.json (if using different images)

Run the conversion script with your full CSV files:

```bash
python convert_stimuli.py \
    --western your_english_images.csv \
    --chinese your_chinese_images.csv \
    --output stimuli.json \
    --n_practice 5
```

### 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial experiment setup"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 4. Import to Cognition.run

1. Go to [cognition.run](https://cognition.run)
2. Create a new experiment
3. Click "Import from GitHub"
4. Enter your repository URL
5. Select `experiment.html` as the main file
6. Deploy!

## Experiment Details

### Task
- 2AFC (two-alternative forced choice)
- Participants judge whether each face image came from a Western (Google) or Chinese (Baidu) source
- Left/Right arrow keys for responses

### Counterbalancing
Key assignments are automatically counterbalanced:
- Version 1: Left = Western, Right = Chinese
- Version 2: Left = Chinese, Right = Western

To assign versions, add `?version=1` or `?version=2` to the URL, or let it randomize automatically.

### Trial Structure
1. Fixation cross (500ms)
2. Face image (until response)
3. [Practice only] Feedback (800ms)

### Data Collected
Each trial records:
- `stimulus`: image path
- `source`: actual source (western/chinese)
- `response`: key pressed
- `response_label`: decoded response (western/chinese)
- `correct`: boolean accuracy
- `rt`: response time (ms)
- `version`: counterbalancing version
- `task`: 'practice' or 'main'

### Breaks
Built-in break screens every 50 trials.

## Customization

### Changing number of practice trials
Edit `convert_stimuli.py` or set `--n_practice` flag.

### Changing break frequency
In `experiment.html`, find `BREAK_INTERVAL` and change the value.

### Adding attention checks
Add stimuli with obvious cues (e.g., visible Chinese text) to the stimuli.json and mark them:
```json
{
    "image": "images/attention/obvious_chinese.jpg",
    "source": "chinese",
    "is_attention_check": true
}
```

Then modify the trial code to flag these.

## Data Analysis

The CSV output includes all trial data. Key columns for analysis:
- Filter by `task == 'main'` for main trials
- `correct` gives accuracy per trial
- `rt` gives response times
- `source` and `response_label` for signal detection analysis (d')

### Quick accuracy calculation (Python):
```python
import pandas as pd

df = pd.read_csv('your_data.csv')
main_trials = df[df['task'] == 'main']

# Overall accuracy
accuracy = main_trials['correct'].mean()

# By source
accuracy_by_source = main_trials.groupby('source')['correct'].mean()

# Signal detection
from scipy.stats import norm
hits = main_trials[(main_trials['source'] == 'chinese') & (main_trials['response_label'] == 'chinese')].shape[0]
fas = main_trials[(main_trials['source'] == 'western') & (main_trials['response_label'] == 'chinese')].shape[0]
# ... calculate d' and c
```

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- No installation required for participants
- Images must be web-accessible (GitHub repo or external hosting)

## Troubleshooting

### Images not loading
- Check that image paths in `stimuli.json` match your folder structure
- Ensure images are committed to the repo (check file size limits)
- GitHub has a 100MB file limit; use Git LFS for large files

### Cognition.run issues
- Make sure `experiment.html` is in the root directory
- Check browser console for JavaScript errors
- Verify stimuli.json is valid JSON (use a JSON validator)

## License

MIT License - feel free to adapt for your research.
