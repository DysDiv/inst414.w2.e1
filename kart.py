"""This program allows the user to insert a link to a reddit thread to gather analysis based on its comments.
Please note that it will create a .csv file with the comments."""
#make sure you have PRAW installed "pip install PRAW"
import praw
#regex is used to parse keywords from comments.
import re
#csv is used to convert dictionaries 
import csv

#reddit information for the KART application script, unique
reddit = praw.Reddit(client_id="I5jAt-s-Bd-KcUN7wSx7Mg",
                     client_secret="CK7QS-TvflNywWB2yVjFLlHpee_Pog",
                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")


def analyze_comments(urls):
    """Takes in a list of target URLs to analyze the keywords within the thread.

    Args:
        urls (list of str): The links to the reddit thread.

    Returns:
        dict: A dictionary containing each keyword, with its respective values in a list:
        [0] number of occurances, [1] cumulative karma, [2] avg karma score
    """
    word_count = {}
    for url in urls:
        submission = reddit.submission(url=url)
        #this line removes the "More Comments" tab from larger threads. Recommend setting limit to something bearable so that run times aren't absurd.
        submission.comments.replace_more(limit=50)
        
        #a list of English stop words to remove
        stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
                    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
                    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
                    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
                    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
                    "with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
                    "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further",
                    "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                    "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                    "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

        for comment in submission.comments.list():
            words = re.findall(r'\b\w+\b', comment.body.lower())  # Extract words using regex
            karma = comment.score
            for word in words:
                if word not in stopwords:
                    if word in word_count:
                        word_count[word][0] += 1  # Increment word count
                        word_count[word][1] += karma  # Add karma score
                    else:
                        word_count[word] = [1, karma]  # Initialize word count and karma score

    for word in word_count:
        word_count[word].append((word_count[word][1])/(word_count[word][0]))
        
        
        sorted_dict = dict(sorted(word_count.items(), key=lambda x: x[1][0], reverse=True))
    return sorted_dict

#as an example, we'll take the top 5 most upvoted posts from r/aww
urls = ["https://www.reddit.com/r/UMD/comments/jl5osc/for_karate_knes144q_we_have_to_record_ourselves/",
        "https://www.reddit.com/r/UMD/comments/hwt715/umd_under_a_thunderstorm/",
        "https://www.reddit.com/r/UMD/comments/ku7wm4/my_inst633_prof_told_us_to_create_oc_posts_for_an/",
        "https://www.reddit.com/r/UMD/comments/j4nn4e/basically_my_entire_first_semester_here/",
        "https://www.reddit.com/r/UMD/comments/13ghmmi/offerings_on_the_first_morning_of_exams/",
        "https://www.reddit.com/r/UMD/comments/l3dayh/warning_for_everyone/",
        "https://www.reddit.com/r/UMD/comments/hegaca/good_karma_for_me_good_karma_for_you_inst_201_meme/",
        "https://www.reddit.com/r/UMD/comments/jq1cc0/maryland_beats_penn_state/"]

word_count = analyze_comments(urls)

#write details into csv
filename = "umd_keywords.csv"

with open(filename, "w", encoding="UTF-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(["Keyword", "Count", "Cumulative Karma", "Avg Karma"])
    
    # Write data
    for key, values in word_count.items():
        writer.writerow([key] + values)
        
print(word_count)