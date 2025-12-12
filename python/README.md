# Projet Bulletin de Solde

**Python/C# hybrid project for automated payslip processing and visualization**

This repository contains a full‑stack system that automates the retrieval, parsing, storage, and visualization of structured payroll documents (bulletins de solde). It demonstrates end‑to‑end engineering skills including automation pipelines, data extraction, database storage, and a web dashboard.

---

## 📌 Project Overview

This project performs the following:

1. **Automated retrieval of payslips** from an email inbox (IMAP).
2. **PDF extraction and data processing** using Python.
3. **Structured storage** of extracted information.
4. **Interactive web dashboard** built with Blazor for visualization.
5. An architecture that separates the pipeline from the presentation layer.

The focus is on backend automation and full‑stack integration rather than front‑end design.

---

## 🧱 Folder Structure

```
Projet-Bulletin-de-Solde/
├── blazor/                  # Blazor web application
│   └── Bulletin_solde2/     # Dashboard UI & logic
├── python/                  # Python ETL pipeline
│   ├── imap_solde_retriever.py   # Email retrieval logic
│   ├── pdf_extract.py            # PDF → CSV / parsed data
│   ├── utils.py                  # Helpers (filename, paths, etc.)
│   └── main.py                   # Main script orchestrating the pipeline
├── modelisation_datetime_arrival.R  # R analysis for modeling arrival dates
├── .gitignore
└── README.md
```
---

## 🚀 Features

### 📬 Automated Email Retrieval

* Connects to an IMAP server.
* Searches for specific emails containing payslip attachments.
* Downloads PDFs and avoids duplicates.

### 📄 PDF Extraction & Parsing

* Extracts structured data from payslip PDFs.
* Converts extracted text into CSV/JSON formats.
* Handles inconsistent document structures and cleaning logic.

### 📊 Web Dashboard (Blazor)

* Interactive charts showing trends over time.
* Summary statistics such as:

  * Total, Average
  * Minimum, Maximum
* Visualizes historical data by month and year.

---

## 🧠 What This Project Shows

This project demonstrates:

* **Automation & ETL pipelines** — retrieval + extraction.
* **Data engineering** — cleaning and structuring unstructured text.
* **Backend & integration logic** — Python + C# communication.
* **Database interaction** via EF Core.
* **Frontend data visualization** with Blazor and charts.
* **Modular, maintainable code structure**, suitable for extension.

This is not a toy script — it is a fully functional, modular pipeline with a visual component.

--- 

## 📊 Statistics Included

* **Total payments**
* **Average payments**
* **Minimum / Maximum payment**
* Support for future stats like median, rolling averages, activity gap detection, etc.

---

## 🗺️ Future Work

The project is ready to be extended with:

* **API layer** using FastAPI or ASP.NET minimal APIs.
* **Automated scheduling** (cron jobs or hosted services).
* **Advanced analytics** (trend prediction, anomaly detection).

---

## 🎯 Why This Is Useful

This project isn’t “just a payslip parser.” It shows the ability to:

* Design and implement a complete data workflow.
* Integrate multi‑language codebases (Python + C#).
* Build interactive dashboards from real data.
* Think like an engineer with separation of concerns and modular architecture.

---

## 🧾 License

This repo is open source and can be reused for educational purposes — as long as sensitive data is handled responsibly.

