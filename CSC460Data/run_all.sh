#!/bin/bash
cd AllScripts
python3 consumptionRates.py
python3 propertyTaxData.py
python3 clean.py
python3 mysqlConnections.py
