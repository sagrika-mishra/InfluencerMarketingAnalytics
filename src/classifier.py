"""
Sponsorship classifier
Classifies YouTube videos as Organic, Implicit, or Explicit sponsorship
based on title and description text.

Validated against 100 manually labelled videos.
"""

import re
import pandas as pd


EXPLICIT_PATTERN = re.compile(r"""
    (thanks?\s*(to)?\s*\w*\s*for sponsoring)|
    (thank you.*(sponsor|sponsoring|sponsored by|for sponsoring))|
    ((this video|segment|channel|content) is sponsored by)|
    (sponsor(ed|ing)?( by)?[:\s-])|
    (ad\s*:?\s*(read|break|spot|slot|segment))|
    (paid\s*(promotion|partnership|collaboration|ad|sponsor))|
    (\[?ad\]?[\s:]+)|
    (use\s+(code|promo|coupon)\s+\w+\s+for)|
    (affiliate\s+link)|
    (#ad\b)|
    (#sponsored\b)|
    (discount\s+code)|
    (promo\s+code)|
    (get\s+\d+%\s+off)|
    (link\s+in\s+(bio|description).*(sponsor|partner|deal|promo))|
    (check\s+out\s+our\s+sponsor)
""", re.IGNORECASE | re.VERBOSE)

IMPLICIT_PATTERN = re.compile(r"""
    (check\s+out\s+[\w\s]+\s+in\s+(the\s+)?description)|
    (link\s+in\s+(the\s+)?description)|
    (affiliate)|
    (partnered?\s+with)|
    (\*\s*some\s+links)|
    (use\s+my\s+(link|code|referral))|
    (referral\s+(link|code|program))|
    (not\s+sponsored\s*,?\s*but)|
    (gifted\b)|
    (c\/o\b)|
    (collab(oration)?\s+with)
""", re.IGNORECASE | re.VERBOSE)


def classify_video(title: str, description: str) -> str:
    """
    Classify a single video as Organic, Implicit, or Explicit.

    Parameters
    ----------
    title : str
        Video title
    description : str
        Video description

    Returns
    -------
    str
        One of 'Explicit', 'Implicit', 'Organic'
    """
    text = f"{title} {description}"

    if EXPLICIT_PATTERN.search(text):
        return "Explicit"
    elif IMPLICIT_PATTERN.search(text):
        return "Implicit"
    return "Organic"


def classify_dataframe(df: pd.DataFrame,
                        title_col: str = "title",
                        desc_col: str = "description") -> pd.DataFrame:
    """
    Classify all videos in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing video metadata
    title_col : str
        Name of the title column
    desc_col : str
        Name of the description column

    Returns
    -------
    pd.DataFrame
        Input DataFrame with added 'Sponsorship' and 'hasSponsorKeywords' columns
    """
    df = df.copy()
    df["Sponsorship"] = df.apply(
        lambda row: classify_video(
            str(row.get(title_col, "")),
            str(row.get(desc_col, ""))
        ),
        axis=1
    )
    df["hasSponsorKeywords"] = df["Sponsorship"] != "Organic"
    return df
