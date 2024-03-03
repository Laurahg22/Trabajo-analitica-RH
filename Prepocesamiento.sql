-- crear tabla general solo con la inforación del 2015
DROP TABLE IF EXISTS general_data2;
CREATE TABLE general_data2 AS 
SELECT * FROM general_data
WHERE strftime('%Y', infoDate) ='2015'
;

-- crear tabla de encuesta de empleados solo con la inforación del 2015
DROP TABLE IF EXISTS employee_survey_data2;
CREATE TABLE employee_survey_data2 AS
SELECT * FROM employee_survey_data
WHERE strftime('%Y',DateSurvey)='2015'
;

-- crear tabla de la encuesta de gerentes solo con la inforación del 2015
DROP TABLE IF EXISTS manager_survey2;
CREATE TABLE manager_survey2 
AS SELECT * FROM manager_survey
WHERE strftime('%Y',SurveyDate) = '2015'
;

-- crear tabla de la variable respueta 'retiros' solo con la inforación del 2016
DROP TABLE IF EXISTS retirement_info2;
CREATE TABLE retirement_info2 AS
SELECT EmployeeID, Attrition FROM retirement_info
WHERE strftime('%Y', retirementDate)='2016' AND retirementType ="Resignation"
;

-- Unir las tablas y consolidadr la base de datos final
DROP TABLE IF EXISTS data_general;
CREATE TABLE data_general AS 
SELECT * FROM general_data2 AS gd
LEFT JOIN employee_survey_data2 AS ee USING (EmployeeID)
LEFT JOIN manager_survey2 AS eg USING (EmployeeID)
LEFT JOIN retirement_info2 AS ir USING (EmployeeID);

-- eliminar columnas que solo tienen valores nulos, además variables que se considera que no aportan inforamción de interés
ALTER TABLE data_general DROP COLUMN ':1'; 
ALTER TABLE data_general DROP COLUMN ':2';
ALTER TABLE data_general DROP COLUMN 'Over18';
ALTER TABLE data_general DROP COLUMN 'StandardHours';
ALTER TABLE data_general DROP COLUMN 'EmployeeCount';

-- convertir variables a dummies 
--attrition
UPDATE data_general
SET Attrition = CASE 
                    WHEN Attrition = 'Yes' THEN 1
                    ELSE 0
                END;

SELECT attrition FROM data_general

-- retirementType  
UPDATE retirement_info
SET retirementType = CASE
						 WHEN retirementtype = 'Resignation' THEN 1
                         ELSE 0
                 END;
                 
SELECT retirementType FROM retirement_info


