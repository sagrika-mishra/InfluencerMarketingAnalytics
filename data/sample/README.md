# Sample Data

This folder contains anonymised sample rows showing the expected schema for each dataset.
Full data files are not included in the repository due to size and privacy constraints.

## channels_data_2024_2025.csv

| Column | Type | Description |
|--------|------|-------------|
| channelId | string | YouTube channel ID (primary key) |
| name | string | Creator name |
| genre | string | Tech or Lifestyle |
| sizeCategory | string | Nano (<100K), Micro (100K-1M), Macro (>1M) |
| subscriberCount | int | Subscriber count at time of collection |
| viewCount | int | Total channel views |
| videoCount | int | Total videos published |
| channelCreationDate | datetime | Channel creation date |
| country | string | Creator country (UK, US, CA, AUS) |
| traditional_videos_12mo | int | Non-Shorts videos in last 12 months |

## videos_data_2024_2025.csv

| Column | Type | Description |
|--------|------|-------------|
| videoId | string | YouTube video ID (primary key) |
| channelId | string | Foreign key to channels |
| creatorName | string | Creator name |
| title | string | Video title |
| description | string | Video description |
| viewCount | int | View count |
| likeCount | int | Like count |
| commentCount | int | Comment count |
| duration_sec | int | Duration in seconds |
| publishedAt | datetime | Upload date |
| genre | string | Tech or Lifestyle |
| sizeCategory | string | Nano, Micro, or Macro |

## comments_data_2024_2025.csv

| Column | Type | Description |
|--------|------|-------------|
| videoId | string | Foreign key to videos |
| channelId | string | Foreign key to channels |
| commentText | string | Comment text |
| commentLikeCount | int | Comment likes |
| commentPublishedAt | datetime | Comment date |

## Derived datasets (output of pipeline)

- **video_engagement_rate_data.csv** — output of notebook 02 (adds Sponsorship column)
- **merged_comments.csv** — output of notebook 03 (adds sentiment_label, sent_score)
- **master_data_27Jul.csv** — output of notebook 04 (full merged dataset for modelling)
- **master_channel_27Jul.csv** — output of notebook 04 (channel-level with subscriber snapshots)
- **cluster_profiles.csv** — output of notebook 05 (cluster assignments per video)
