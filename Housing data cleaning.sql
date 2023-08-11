--

-- Cleaning data in SQL queries

--
USE portfolioDB
GO
SELECT *
FROM NashvilleHousing




-- 1 | Standardize date format (sale date) | --

SELECT saledate, CONVERT(date,saledate)
FROM NashvilleHousing

ALTER TABLE NashvilleHousing
ADD SaleDateConverted DATE;

UPDATE NashvilleHousing
SET SaleDateConverted = CONVERT(date,SaleDate)




-- 2 | Property address data | --

SELECT *
FROM NashvilleHousing
WHERE PropertyAddress is null

SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM NashvilleHousing a
JOIN NashvilleHousing b
ON a.ParcelID = b.ParcelID
AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress is null

UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM NashvilleHousing a
JOIN NashvilleHousing b
ON a.ParcelID = b.ParcelID
AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress is null




-- 3 | Breaking out address into individual columns (Address, City, State) | --

SELECT PropertyAddress
FROM NashvilleHousing

SELECT
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) AS Address, 
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress)) AS Address

FROM NashvilleHousing
ALTER TABLE NashvilleHousing
ADD PropertySplitAddress NVARCHAR(255);
UPDATE NashvilleHousing
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)

ALTER TABLE NashvilleHousing
ADD PropertyCity NVARCHAR(255);
UPDATE NashvilleHousing
SET PropertyCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress))

SELECT PARSENAME(REPLACE(OwnerAddress, ',', '.'),1)
FROM NashvilleHousing


ALTER TABLE NashvilleHousing
ADD OwnerSplitAddress NVARCHAR(255);
ALTER TABLE NashvilleHousing
ADD OwnerSplitCity NVARCHAR(255);
ALTER TABLE NashvilleHousing
ADD OwnerSplitState NVARCHAR(255);

UPDATE NashvilleHousing
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',', '.'),3)

UPDATE NashvilleHousing
SET OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress, ',', '.'),2)

UPDATE NashvilleHousing
SET OwnerSplitState = PARSENAME(REPLACE(OwnerAddress, ',', '.'),1)




-- 4 | Change Y and N to Yes and No in "Sold as vacant" field | --

SELECT DISTINCT(SoldAsVacant), COUNT(SoldAsVacant)
FROM NashvilleHousing
GROUP BY SoldAsVacant
ORDER BY 2

Select SoldAsVacant,
CASE WHEN SoldAsVacant = 'Y' THEN 'Yes'
	WHEN SoldAsVacant = 'N' THEN 'No'
	ELSE SoldAsVacant
	END
FROM NashvilleHousing

UPDATE NashvilleHousing
SET SoldAsVacant = CASE WHEN SoldAsVacant = 'Y' THEN 'Yes'
	WHEN SoldAsVacant = 'N' THEN 'No'
	ELSE SoldAsVacant
	END




-- 5 | Remove duplicates | --

WITH RowNumCTE AS(
		SELECT *,
			ROW_NUMBER() OVER 
				(PARTITION BY ParcelID, PropertyAddress, SalePrice, SaleDate, LegalReference
				 ORDER BY UniqueID) row_num
				 FROM NashvilleHousing
				 )

DELETE
FROM RowNumCTE
WHERE row_num > 1
--ORDER BY PropertyAddress

SELECT *
FROM RowNumCTE
WHERE row_num > 1
--ORDER BY PropertyAddress




-- 6 | Delete unused columns | --

SELECT *
FROM NashvilleHousing


ALTER TABLE NashvilleHousing
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress, SaleDate

