# AlgicideDB

AlgicideDB is a comprehensive, manually curated database for algicidal compounds and their effects on harmful algal blooms (HABs). This platform (available at http://algicidedb.ocean-meta.com/#/) provides valuable resources for researchers and practitioners working on HAB control and management.

## Overview

Harmful algal blooms (HABs) are becoming more frequent and intense worldwide, posing serious threats to aquatic ecosystems, fisheries, and human health. While chemical algicides are widely used to control HABs due to their fast-acting nature, concerns about their environmental toxicity and the lack of comprehensive data integration limit their broader use.

AlgicideDB addresses these challenges by providing:
- A manually curated database containing 1,672 algicidal records from 204 publications
- Coverage of 542 algicides targeting 110 algal species
- An algicide-likeness scoring system for identifying compounds with potential antialgal properties
- Integration with a large language model powered by the HABs knowledge base

## Features

### Database Content
- Comprehensive collection of algicidal compounds and their effects
- Detailed information on algal species, including:
  - Taxonomic classification
  - Environmental characteristics
  - Risk assessment
  - Visual documentation
- Chemical compound data including:
  - Molecular properties
  - Classification
  - Origin (Animal, Plant, Microorganism, Chemical)
  - CAS numbers
  - SMILES structures

### Key Tools
1. **Molecular Property Prediction**
   - Quantitative Estimation of Algicide-Likeness (QEF)
   - Calculation of key molecular properties:
     - Molecular weight
     - Octanol-water partition coefficient (logP)
     - Number of hydrogen bond acceptors (HBA)
     - Number of hydrogen bond donors (HBD)
     - Number of rotatable bonds (nRotB)
     - Number of aromatic rings (nArR)
   - Integration with AdmetLab Service for advanced aquatic toxicity predictions

2. **Search and Analysis**
   - Advanced search capabilities across multiple parameters
   - Detailed record visualization
   - Export functionality for research and analysis

## Technical Architecture

The project consists of two main components:

### Backend (AlgicideDB_backend)
- Built with Django 4.2.8
- RESTful API architecture
- PostgreSQL database
- Key models include:
  - AlgaeSpecies
  - Chemical
  - Record
  - Reference
  - AlgaeStrain

### Frontend (AlgicideDB_frontend)
- Modern Vue.js application
- Responsive design
- Interactive data visualization
- User-friendly interface for data exploration

## Getting Started

### Prerequisites
- Python 3.x
- Node.js and npm
- SQLite
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd AlgicideDB
```

2. Backend Setup:
```bash
cd AlgicideDB_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. Frontend Setup:
```bash
cd AlgicideDB_frontend
npm install
npm run serve
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 