# Limerick Council Meetings

This repository contains texts extracted all publically available meeting agendas and minutes from Limerick City and County Council. These are generated by PDFs that are uploaded to https://www.limerick.ie/council/your-council/meetings

The purpose of this repo is to allow easy searching of the contents of these PDFs by utilizing github's built in search functionality. It also may be easier to navigate to meetings on specific dates as the limerick.ie website only supports navigation one month at a time.

## Why?
Transparency in local government is essential to a healthy democracy. While official minutes are available, they can be difficult to find, navigate, and search through. This project aims to make these records more accessible, searchable, and user-friendly — helping to bridge the gap between the council's decisions and the community it serves.

## Notes
Scanned pages are read using basic OCR and as such the contents are likely to be inaccurate. These pages have a disclaimer at the top in the markdown.

Files are located in the meeting as they are uploaded to limerick.ie as such minutes will be associated with the meeting where they were adopted rather than the meeting they were recorded. 

When searching across in a year folder minutes for meetings near the end of the year are likely to be adopted at the next relevant meeting in the year after.

Images in PDFs are currently omitted to ensure searching is easier. They will be marked with (Image omitted). To view these images you will need to navigate to the meeting 

## Search Tips
You must have a GitHub account and be signed in to use GitHub's search feature

Using GitHub's search functionality, you can search for words or phrases. e.g.
![example](https://i.imgur.com/7GIuqQF.png)

From here you will see various instances where this word appears in documents.

You can further refine the search into relevant paths by clicking one of the "Paths" shown above on the left. This for example can limit the search now to only files from meetings in 2022 

Searching multiple words will only show files where all those words are present anywhere in the file.

If you want to search a specific phrase you should wrap it in quotation marks.

`"bus lane"`

### Useful additional parameters
Additional parameters can be included in a search
#### Search a year/month:
To search only files from meetings in 2024

`path:meetings/2024`

This is very effective for agendas however remember that minutes are stored in the meeting they are adopted, not the meeting they were recorded in. As such minutes for meetings at the end of the year are likely to be stored in the following year.

It may be more effective to search for year anywhere in the path but this may give results from a slightly larger range.

`path:**/*2024*`

To search only files from meetings in September 2023

`path:meetings/2023/09`

#### Searching a specific districts meetings
Use one of the following to limit searches to a specific district.

`path:**/*Limerick City and County*`

`path:**/*Metropolitan*`

`path:**/*Cappamore-Kilmallock*`

`path:**/*Adare-Rathkeale*`

`path:**/*Newcastle West*`

#### Case sensitive
Add the following to make searches case sensitive

`case:true`

## Creation
This is created by using https://github.com/FarronF/limerick-council-tools

## Potential improvements to this repo:

README.md files at each level to allow for better visibility of meetings in child folders.

More PDFs. (replies to questions next)

Better OCR for scanned pages to improve accuracy. (this may be hard due to my limited hardware)

Normalise file names for consistancy in searching.

Possibly store minutes in the folder for the meeting they were recorded from rather than when they were adopted. This might make searching by year easier but could introduce new challenges.

## Feedback
If you have feedback for this project feel free to message me directly or open a GitHub discussion on the repo.

## Support
If this project is useful, feel free to let me know. Star the repo. 

Or if you really want, you can support the project through Ko-Fi by clicking the button below. This will go towards renting a virtual machine for better OCR of those badly scanned PDFs.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/farronf)
