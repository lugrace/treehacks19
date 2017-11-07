# EUPHORIA: Student Happiness
Made with <3 for Technica 2017 Hackathon

# INSPIRATION
As high school seniors (and one junior!) who recently applied to the colleges, we discovered that you can't learn about a college's community from just academics or rankings. We wanted to know what students were saying about their college, and if it was a depressive/supportive environment. Designed for prospective students and curious parents, Euphoria analyzes the happiness and interests of students on campus, allowing you to see if you'll fit right in.

# WHAT IT DOES 
First, enter a college you're interested in. We take in this information and search twitter for recent tweets that have mentioned your school (acronyms and all). Then by using Natural Language Processing and Microsoft Azure's Cognitive Text Analysis API, we analyzed these tweets and quantitatively represent the positivity/negativity of them. After averaging the data, we can determine the overall feel of the student body in real-time. You get to see the overall happiness percentage, knowing that the higher the number, the happier the college students are. We've also included separated outlier negative and positive percents. There's a few tweets shown to give you a better picture of student life. Finally, relevant key words relating to student life are organized to inform you of what the community is currently talking about and interested in.

# BUILT WITH
Front-end: HTML, CSS, Javascript
Back-end: Python
Framework: Django
