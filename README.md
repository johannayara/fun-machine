# Cartographie des revenus dans les quartiers de Lausanne
## Description du projet
Ce projet vise à analyser l'évolution des revenus dans les quartiers de Lausanne au cours du XXe siècle. Pour ce faire, nous avons constitué une base de données regroupant les salaires mensuels moyens par secteur, catégorie professionnelle et année. Nous avons ensuite classé les métiers issus des annuaires dans nos catégories, puis associé chaque personne à un salaire correspondant.

À l'étape suivante, nous avons utilisé Nominatim pour géolocaliser les individus sur une carte de Lausanne.

Le projet s’appuie sur des bibliothèques Python standard, ainsi que sur NumPy, Pandas, Nominatim, le jeu de données de la HES-SO, et les annuaires lausannois.

## Structure du projet
```
.
├── LICENSE
├── README.md
├── classification/
│   └── classification_results.csv
├── data/
│   ├── SHS_TM.csv
│   ├── SHS_TM.xlsx # original salary data 
│   ├── all_metiers.csv
│   ├── category_mappings.csv
│   ├── final_test.csv
│   ├── indicateur_1885.txt
│   ├── indicateur_1901.txt
│   ├── indicateur_1923.txt
│   ├── indicateur_1951.txt
│   ├── metier_to_annee.csv
│   ├── table_1885.csv
│   ├── table_1885_clf.csv
│   ├── table_1901.csv
│   ├── table_1901_clf.csv
│   ├── table_1923.csv
│   ├── table_1923_clf.csv
│   ├── table_1923_v3-1_geoloc.xlsx
│   ├── table_1951.csv
│   ├── table_1951_clf.csv
│   └── test.csv
├── data_processing/
│   ├── heatmap/
│   │   ├── intensity_data.js
│   │   ├── intensity_data.json
│   │   └── prepare_data.py
│   └── topjobs/
│       └── process_jobs.py
├── failed_attemps/
│   ├── kmeans_metiers.ipynb
│   └── mapping_job_salaire.ipynb
├── geocoding/ # everything related to geocoding data 
│   ├── cache/
│   │   └── geocode_cache.pkl
│   ├── data/ # non-geocoded data 
│   │   ├── table_1885_clf.csv
│   │   ├── table_1901_clf.csv
│   │   ├── table_1923_clf.csv
│   │   └── table_1951_clf.csv
│   ├── errors/ # error files representing points that we failed to locate 
│   │   ├── geocode_errors_1901.csv
│   │   ├── geocode_errors_1923.csv
│   │   └── geocode_errors_1951.csv
│   ├── geolocate.py # script to geocode the data 
│   └── out/ # geocoded data 
│       ├── geocoded_table_1901_clf.csv
│       ├── geocoded_table_1923_clf.csv
│       └── geocoded_table_1951_clf.csv
├── notebooks/
│   ├── generate_answer.ipynb
│   ├── map_job_salary.ipynb
│   └── plot_salaries.ipynb
├── plots/
│   ├── avg.png
│   └── sectors.png
└── top_jobs/
    ├── top_jobs1885.csv
    ├── top_jobs1901.csv
    ├── top_jobs1923.csv
    └── top_jobs1951.csv

```

## Mise en place 

### Cloner le repo

#### Via HTTPS:
```bash
git clone https://github.com/johannayara/fun-machine.git
```

#### Via SSH:
```bash
git clone git@github.com:johannayara/fun-machine.git
```
---