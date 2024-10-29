# JobHuntr (Job Application Tracker)

## Overview
JobHuntr is a web application built with Flask, Python, Bootstrap, and SQLite, designed to help users manage their job applications efficiently. The application allows users to track jobs they want to apply for, monitor their application statuses, and organize their job search effectively.

## Features
- **User Authentication**: Users can register for an account, log in, and manage their profile.
- **Job Management**:
  - **Add Job**: Users can add jobs they want to apply for, along with optional contact information.
  - **Overview Page**: Displays all added jobs in a table format.
  - **Filtered Views**: Users can navigate through different views:
    - **To Apply**: Jobs the user has added but not applied for yet.
    - **Submitted**: Jobs the user has applied for but hasn't received a response for yet.
    - **Interviewing**: Jobs for which the user is interviewing or has interviewed but is waiting for a response.
    - **Archived**: Jobs that have expired, been rejected, or resulted in a job offer.
- **Job Status Management**: Easily change the status of jobs using a toggle menu.
- **Job Options**: Each job has buttons for "More Info," "Edit," and "Delete."
  - **More Info**: Opens a modal displaying full job information.

