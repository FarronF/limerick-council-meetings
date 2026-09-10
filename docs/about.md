# Limerick Council Meetings Archive

[![Ko-Fi Support](https://img.shields.io/badge/Support-Ko--Fi-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/farronf)
[![License: Open Data](https://img.shields.io/badge/Data-Public%20Domain-blue.svg)](#important-notes-on-the-data)

An open, searchable repository and documentation hub for extracted text from all publicly available meeting agendas and minutes published by Limerick City and County Council.

---

## Project Overview

While official agendas and minutes are uploaded to [limerick.ie](https://www.limerick.ie/council/your-council/meetings), finding specific records can be frustrating. The official portal relies on a poorly designed calendar interface that limits navigation to a single month at a time, and key council decisions remain locked inside separate PDF files across multiple years.

This project extracts text from those official PDFs and organizes them into an indexed directory structure. This allows users to search, filter, and analyze years of local government records instantly.

---

## Why This Exists

Local government transparency is essential to a healthy democracy. Every month, decisions are made that impact housing, public transit, climate action, cultural funding, and local infrastructure across Limerick.

By making these public records directly searchable, this project aims to bridge the gap between council actions and the community it serves. Whether you are a resident, journalist, researcher, or community activist, finding specific policy discussions, voting records, or district updates shouldn't require fighting a clunky calendar widget or downloading dozens of PDFs.

---

## How to Search

The site uses Pagefind to provide fast, full-text client-side searching across all meeting documents.

### 1. Keyword and Exact Phrase Matching

Enter terms in the search bar. Use double quotes to find exact phrases:

- `"bus lane"`
- `"active travel"`
- `"housing estate"`

### 2. Filtering by Date

Use the sidebar filters generated on the search page to restrict results by time period:

- **By Year:** Select a specific year (e.g. `2024`) from the **Year** filter.
- **By Year and Month:** Select a specific month (e.g. `2023-09`) from the **Year-Month** filter.

### 3. Filtering by Council Body or District

Narrow your search to specific municipal districts or strategic policy committees using the **Council Body** filter:

| District / Body            | Filter Option                                              |
| :------------------------- | :--------------------------------------------------------- |
| **Full Council (Plenary)** | Select `Limerick City and County Council`                  |
| **Metropolitan District**  | Select `Metropolitan District`                             |
| **Adare-Rathkeale**        | Select `Adare-Rathkeale`                                   |
| **Cappamore-Kilmallock**   | Select `Cappamore-Kilmallock`                              |
| **Newcastle West**         | Select `Newcastle West`                                    |
| **Committees**             | Select `Environment SPC`, `Joint Policing Committee`, etc. |

### 4. Filtering by Document Type

You can also filter results by **File Type** (`Agenda`, `Minutes`, `Meeting Overview`) or **Meeting Type** (`Regular`, `Special`, `Annual`).

---

## Important Notes on the Data

- **Scanned PDFs & Accessibility:** The council regularly uploads scanned image-based PDFs rather than text-based documents. This poses a major digital accessibility barrier for screen readers and search engines alike. OCR (Optical Character Recognition) is used here to extract the text, which makes the content accessible, though minor parsing errors can occur. Affected files contain an OCR disclaimer in their header.
- **Minutes Association:** Documents are organized according to when they were uploaded or formally adopted by the council. Minutes are typically stored in the directory of the meeting where they were _approved_, which means end-of-year minutes may appear under the following year's folder.
- **Omitted Images:** Images, maps, and diagrams are omitted to keep the repository search-friendly and lightweight. These are marked inline as `(Image omitted)`. Refer to the original PDF on limerick.ie for visual context.

---

## Technical Details and Pipeline

- Processing pipeline generated using [limerick-council-tools](https://github.com/FarronF/limerick-council-tools).
- Directory structure: `docs/meetings/YYYY/MM/DD_Meeting_Name/`
- Search indexing powered by [Pagefind](https://pagefind.app/).

---

## Roadmap and Future Enhancements

- Add overview summaries at every folder level for enhanced navigation.
- Integrate additional PDF types (e.g., formal written replies to questions).
- Upgrade OCR processing models to improve accuracy across scanned council PDFs.
- Standardize file-naming conventions for consistent indexing.

---

## Feedback and Support

- **Feedback and Ideas:** Open a discussion or issue in this repository.
- **Star the Repo:** If this resource helps your research, starring the project helps increase its visibility.
- **Support Processing Costs:** Running OCR processing and infrastructure requires hardware resources. If you would like to help support those server costs, you can contribute via Ko-Fi:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/farronf)
