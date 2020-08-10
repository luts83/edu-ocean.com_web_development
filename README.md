# www.edu-ocean.com
## E-learning Platform Design

### The website is built with HTML and Python programming language on top of the Django framework. The Django framework was chosen to shorten the time it takes to develop the site considering the given timeline. The most popular front-end framework ‘Bootstrap’ is used to build a responsive web and distributed via AWS. 

- Django: Django is an open source web application framework coded with Python programming language. It follows the Model View Controller (MVC) patterns. It provides predefined templates for important functions which enables a rapid development without custom coding involved. 

- Bootstrap: Bootstrap framework includes the most commonly used web elements and it supports both the desktop and mobile design, which makes development quicker and simpler. With this framework, websites that supports various browsers can be developed within a relatively short time frame. 

- AWS: Amazon Web Services by Amazon provides on-demand cloud computing platforms including virtual machines, storage, infrastructure, and so on based on the network it has.

- EC2: Amazon Elastic Compute Cloud (Amazon EC2) is a part of cloud-computing services that rent out virtual computers to users. With Amazon EC2, users can develop and distribute applications without investing in hardware and conveniently build a virtual server and manage private, network and storage on Amazon EC2. It is flexible in expanding or downsizing the scale swiftly for unexpected surge in requests and demand, which makes server traffic forecast unnecessary.

- RDS: Amazon Relational Database Service (Amazon RDS) is a distributed relational database service designed to simplify the setup, operation, and scaling of a relational database for use in applications (Amazon website). This service provides economical and flexible storage for industrial relational database and database management. RDS provides Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle Database, and SQL Server and MySQL is used for this experiment.

### User Interface Description

Based on findings in the section above, functionalities listed below that supplement the shortcomings of the third party platform are added to measure the factors that are expected to have impact on learnings. 
![에듀오션 UI 그림 (2)](https://user-images.githubusercontent.com/63055047/89772300-b2d16280-daf9-11ea-945d-d25432586523.png)
- Assignment Updates
The announcement section is placed at the top of the page so that the visitors can check the updates as soon as they land on the learning page. The participants can check the updates and download the assignments, tutorial announcements, and learning materials that are uploaded by the tutor every week.

- Contents (Study Materials)
It consists of the recorded lecture (filmed by the tutor) and an audio file for speaking practices. In the case of the recorded lecture that is displayed in an iframe on page, the video is uploaded to the YouTube channel so that it can be viewed even after the class is completed.

- Vocabulary Test
A list of important vocabulary is handpicked by the tutor. The participants are required to take a quiz that is created as a form of flash card. 

- Test Score & Progress
The participants are able to view their own test scores and the average score of other participants in the study group, and the assignment progress of others. This section is designed to expose participants to others’ progres and give motivations by comparing themselves with others and feeling healthy pressure to complete their goals.

- Assignment Submission
Utilising the learning materials provided weekly by the tutor, the participants can do a self-paced study within a deadline and submit the assignment which will update the progress bar when the files are uploaded. Only the tutor can view the file and leave comments.

- Comments
It is designed to enable communications between the tutor and the participants. Unlike the instant messenger platform, it excluded the function that participants can communicate with each other. Most importantly, in order to validate the hypothesis, two groups were recruited; one group of people who want a feedback on their assignment from the tutor and the other group who don’t.

- Assignment Submission Page
On this page, participants can upload image files of the notes they took while watching the video class and an audio file that recorded their speaking practice, Once the files are uploaded, it marks the participant’s assignment as ‘completed’.  

- Vocabulary Test Page
On the vocabulary test page, 30-50 words shortlisted by the tutor will be prompted randomly like a flash card. It can be attempted repeatedly, but the last attempt will be recorded as the final score. All the records is stored in the database for analysis of the change of the scores over time and if it has any relationship with the completion of the assignment.
