# Rate My Professor
[![Build Status](https://travis-ci.com/umcssa/rate-my-professor.svg?branch=master)](https://travis-ci.com/umcssa/rate-my-professor)

A web application produced by the CSSA APPs development team. Students at the University of Michigan can use RMP to give comment to their professors and courses, as well as search other students' comment records.

## Website
[http://app.um-cssa.org/rate-my-professor/](http://app.um-cssa.org/rate-my-professor/)

## Development Setup
* Preparation
```
git clone https://github.com/umcssa/rate-my-professor.git
cd rate-my-professor
```
* Back-end in Flask
```
cd server
python3 -m venv env
source env/bin/activate
pip install -e .
./bin/rmprun
```
* Front-end in React
```
cd client
npm install
npm start
```

## Contributing
If you are a member of UM-CSSA and have passion for web development, welcome to join our CSSA APPs development team! Please contact [kezian@umich.edu](mailto://kezian@umich.edu).
