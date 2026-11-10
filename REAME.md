# ShopSense: E-commerce Product Intelligence and Review Analyzer

A data analytics internship project covering four tasks in one pipeline: web scraping, exploratory data analysis, data visualization, and sentiment analysis. Results are shown in a Streamlit dashboard.

## Data sources (please read)

- **Reviews:** 50 practice reviews for about 25 earbuds products. This is generated practice data, **not real customer data**.
- **Scraping:** `requests` and `BeautifulSoup` on [books.toscrape.com](https://books.toscrape.com), a site built for scraping practice (11 books, title and price). It demonstrates the technique; it contains no reviews.

Findings below describe the method on a small sample. They are not claims about the real earbuds market.

## What the project does

1. **Scraping:** fetch a page, extract fields, save to CSV.
2. **Cleaning and EDA:** found and removed 1 junk row (51 to 50 rows), kept 3 reviews with missing ratings, checked duplicates, rating distribution, rating vs sentiment, price vs rating.
3. **Visualization:** Matplotlib charts in notebooks, Plotly charts in the dashboard.
4. **Sentiment analysis:** VADER baseline, plus an aspect-based baseline (keyword matching, reviews split at "but").

## Results (50-review practice sample)

- Sentiment: 32 positive, 9 neutral, 9 negative.
- Average rating by sentiment: negative 1.71 (7 rated reviews), neutral 3.00 (8), positive 4.13 (32).
- Price vs average rating: correlation 0.36, weak, each product has only 1-2 ratings.
- VADER check on the first 18 reviews with my own labels: accuracy 0.83 (15 of 18), neutral F1 0.57. Too few reviews to call this a reliable accuracy.

## Limitations

- Practice data and a small sample.
- Evaluation covers only 18 reviews, labelled by one person.
- Custom lexicon scores (for words like "drains", "overpriced") are tuned guesses, not evaluated.
- Aspect-level accuracy has not been measured.
- Aspect keywords are hand-written, so reviews using other words are missed.

## Project structure
notebooks/   Jupyter notebooks (load, cleaning, scraping, EDA, visualization, sentiment, aspects)
data/raw/    original and scraped data
data/processed/   cleaned data and sentiment results
app/app.py   Streamlit dashboard
.streamlit/  dashboard theme

## Run the dashboard

pip install -r requirements.txt
python -m streamlit run app/app.py

Run the command from the project root folder.

## Tech

Python, Requests, BeautifulSoup, Pandas, Matplotlib, Plotly, NLTK (VADER), scikit-learn, Streamlit.