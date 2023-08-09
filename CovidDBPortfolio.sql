SELECT *
FROM CovidDB..CovidDeaths
WHERE continent is not null
ORDER BY 3,4

--SELECT *
--FROM CovidDB..CovidVaccinations
--ORDER BY 3,4

-- Select the data for use

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM CovidDB..CovidDeaths
WHERE continent is not null
ORDER BY 1,2

-- Looking at Total cases vs Total deaths
-- Shows likelihood of dying if you contract COVID in Argentina
SELECT location, date, total_cases, total_deaths, (CONVERT(int,total_deaths)/CONVERT(int,total_cases))*100 AS DeathPercentage
FROM CovidDB..CovidDeaths
--WHERE location like 'Argentina'
WHERE continent is not null
ORDER BY 1,2


-- Looking at Total cases vs Population
-- Shows what percentage of population got COVID
SELECT location, date, total_cases, population, (CONVERT(bigint,total_cases)/CONVERT(bigint,population))*100 AS InfectedPopulationPercentage
FROM CovidDB..CovidDeaths
--WHERE location like 'Argentina'
WHERE continent is not null
ORDER BY 1,2


-- Looking at countries with Highest infection rate compared to population
SELECT location, population, MAX(CONVERT(bigint,total_cases)) as HighestInfectionCount, Max((CONVERT(bigint,total_cases)/CONVERT(bigint,population)))*100 AS InfectedPopulationPercentage
FROM CovidDB..CovidDeaths
WHERE continent is not null
GROUP BY location, population
ORDER BY InfectedPopulationPercentage desc


-- Showing Countries with the highest death count per population
SELECT location, MAX(CONVERT(bigint,total_deaths)) as TotalDeathCount
FROM CovidDB..CovidDeaths
WHERE continent is not null
GROUP BY location
ORDER BY TotalDeathCount desc


-- Showing continents with the highest death count per population
SELECT continent, MAX(CONVERT(bigint,total_deaths)) as TotalDeathCount
FROM CovidDB..CovidDeaths
WHERE continent is not null
GROUP BY continent
ORDER BY TotalDeathCount desc


-- GLOBAL NUMBERS

SELECT date, SUM(new_cases) as total_cases, SUM(CONVERT(bigint,new_deaths)) as total_deaths,
			CASE 
			WHEN SUM(new_cases) > 0 THEN 
				(SUM(CONVERT(bigint, new_deaths)) * 100.0) / SUM(new_cases)
			ELSE
				NULL
			END AS DeathPercentage
FROM CovidDB..CovidDeaths
WHERE continent is not null
GROUP BY date
ORDER BY 1,2



-- Looking at Total population vs Vaccinations

WITH PopvsVac (Continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPeopleVaccinated
FROM CovidDB..CovidDeaths dea
JOIN CovidDB..CovidVaccinations vac
ON dea.location = vac.location and dea.date = vac.date
WHERE dea.continent is not null
--ORDER BY 2,3
)
SELECT *,(RollingPeopleVaccinated/population*100) 
FROM PopvsVac
AS VacPercentage


-- Creating VIEWS to store data for later visualizations
USE CovidDB
GO
CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPeopleVaccinated
FROM CovidDB..CovidDeaths dea
JOIN CovidDB..CovidVaccinations vac
ON 
	dea.location = vac.location
	and
	dea.date = vac.date
WHERE dea.continent is not null


SELECT * 
FROM PercentPopulationVaccinated