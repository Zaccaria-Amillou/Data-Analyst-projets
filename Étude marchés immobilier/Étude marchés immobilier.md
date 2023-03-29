## Mise en situation 
Vous êtes data analyst chez Laplace Immo, un réseau national d’agences immobilières. Le directeur général est sensible depuis quelque temps à l’importance des données, et il pense que l’agence doit se démarquer de la concurrence en créant un modèle pour mieux prévoir le prix de vente des biens immobiliers. 

## Objectives
1. Préparer le dicionnaire des données 
2. Créer le schema relationnel (UML)
3. Créer la base de données (BDD)
4. Effectuer des requêtes dans la BDD

## Requêtes en SQL

**1. Nombre total d’appartements vendus au 1er semestre 2020.**
```sql
SELECT 
	count(v.id_vente) AS "No appartements vendus au 1er semestre 2020"
FROM 
	vente v
	JOIN bien b
		ON v.id_bien = b.id_bien
WHERE
	v.date BETWEEN '2020-01-01' AND '2020-07-01'
	AND
	b.type_local LIKE 'Appartement';
  ```

**Résultats**

![Pasted image 20230316105522.png](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105522.png)

**2. Le nombre de ventes d’appartement par région pour le 1er semestre
2020**
```sql
SELECT 
	r.code_reg "Code région", 
    r.reg_nom AS "Nom région", 
    count(id_vente) as "No ventes"
FROM 
	bien b
	JOIN vente v 
		ON b.id_bien = v.id_bien
	JOIN commune c
		ON b.id_codedep_codecommune = c.id_codedep_codecommune
	JOIN region r
		ON c.code_reg =  r.code_reg
WHERE 
	b.type_local LIKE "Appartement"
	AND
	v.date BETWEEN '2020-01-01' AND '2020-07-01'
GROUP BY r.code_reg
ORDER BY count(id_vente) DESC
;
```

**Résultats**

![Pasted image 20230316105549.png](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105549.png)

**3. Proportion des ventes d’appartements par le nombre de pièces.**
```sql
SELECT 
	no_pieces AS 'No pieces', 
	ROUND((COUNT(*)/(SELECT COUNT(*) FROM bien WHERE type_local = "Appartement")*100),2) AS "poportion appartements vendus"
FROM 
	bien b
	JOIN vente v
		ON b.id_bien = v.id_bien
WHERE 
	b.type_local = "Appartement"
GROUP BY b.no_pieces
ORDER BY no_pieces ASC;
```

**Résultats**

![Pasted image 20230316105638.png](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105638.png?raw=true)

**4. Liste des 10 départements où le prix du mètre carré est le plus élevé.**
```sql
SELECT 
	code_dep AS "Département",
	ROUND(AVG(v.valeur/b.surface_carrez),2) AS 'prix_m2'
FROM 
	bien b
	JOIN commune c
		ON b.id_codedep_codecommune = c.id_codedep_codecommune
	JOIN vente v
		ON b.id_bien = v.id_bien
WHERE 
	surface_carrez > 0
GROUP BY code_dep
ORDER BY prix_m2 DESC
LIMIT 10;
```

**Résultats**

![Pasted image 20230316105738.png](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105738.png?raw=true)


**5. Prix moyen du mètre carré d’une maison en Île-de-France.**
```sql
SELECT 
	ROUND(AVG(v.valeur/b.surface_carrez),2) AS 'prix moyenne m2 maison en Ile de France'
FROM 
	bien b
	JOIN vente v
		ON v.Id_bien = b.Id_bien
	JOIN commune c 
		ON b.id_codedep_codecommune = c.id_codedep_codecommune
WHERE code_reg = '11'
AND type_local = 'Maison';
```

**Résultats**

![[Pasted image 20230316105758.png]](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105758.png?raw=true)

**6. Liste des 10 appartements les plus chers avec la région et le nombre
de mètres carrés.**
```sql
SELECT 
	r.reg_nom AS "Nom région", 
    b.id_bien AS "id appartement", 
    no_voie AS 'n', 
    type_voie AS "type", 
    voie,  
    v.valeur,
    ROUND(surface_carrez,2) AS m2
FROM 
	bien b
	JOIN vente v
		ON b.id_bien = v.id_bien
	JOIN commune c
		ON b.id_codedep_codecommune = c.id_codedep_codecommune
	JOIN region r
		ON c.code_reg = r.code_reg
WHERE type_local = "Appartement"
ORDER BY v.valeur DESC
LIMIT 10;
```

**Résultats**

![Pasted image 20230316105821.png](https://github.com/Zaccaria-Amillou/Data-Analyst-projets/blob/main/%C3%89tude%20march%C3%A9s%20immobilier/images/Pasted%20image%2020230316105821.png?raw=true)

**7. Taux d’évolution du nombre de ventes entre le premier et le second
trimestre de 2020.**
```sql
WITH 
trim1 AS (
	SELECT COUNT(id_vente) AS t1 FROM vente where MONTH(date) BETWEEN 1 AND 3),
trim2 AS (
	SELECT count(id_vente) AS t2 FROM vente where MONTH(date) BETWEEN 4 AND 6)
    
SELECT 
	t1 AS 'Trimestre 1', 
    t2 AS 'Trimestre 2', 
    ROUND(((t2-t1)/t1)*100, 2) AS 'Taux evolution nombre vente'
FROM trim1, trim2;
```

**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228474867-feadcd24-4fc2-4a29-8687-ff20bfc4caa8.png)

**8. Le classement des régions par rapport au prix au mètre carré des
appartement de plus de 4 pièces**
```sql
SELECT 
	r.code_reg AS "Code région",
    reg_nom AS "Région", 
    ROUND(AVG(v.valeur/b.surface_carrez),2) AS Prix_m2
FROM bien b 
    JOIN vente v 
		ON b.id_bien = v.id_bien 
    JOIN commune c
		ON c.id_codedep_codecommune = b.id_codedep_codecommune
	JOIN region r
		ON r.code_reg = c.code_reg
WHERE 
	b.no_pieces > 4 
	AND 
	type_local LIKE "Appartement"
    AND 
    surface_carrez > 0
GROUP BY r.code_reg
ORDER BY Prix_m2 DESC;
```

**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228475011-bb70acaa-fd7c-4c4b-8e06-4375bfb68b4a.png)

**9. Liste des communes ayant eu au moins 50 ventes au 1er trimestre**
```sql
SELECT 
	c.nom_commune AS "Commune", 
    COUNT(v.id_vente) AS Ventes
FROM bien b
	JOIN vente v
		ON b.id_bien = v.id_bien
	JOIN commune c
		ON c.id_codedep_codecommune = b.id_codedep_codecommune
WHERE 
	MONTH(date) BETWEEN 1 AND 3

GROUP BY c.nom_commune
HAVING Ventes >= 50 
ORDER BY ventes ASC;
```

**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228475129-804c4ca6-2c4c-448b-91a9-1f169130b636.png)

**10. Différence en pourcentage du prix au mètre carré entre un
appartement de 2 pièces et un appartement de 3 pièces.**
```sql
SELECT 
		ROUND(AVG(v.valeur/b.surface_carrez),2) AS Prix_m2_2p
        FROM 
			bien b
			JOIN vente v 
				ON b.id_bien = v.id_bien
        WHERE 
			b.no_pieces = 2
			AND 
			type_local = "Appartement"),
	3pieces AS (
    SELECT 
		ROUND(AVG(v.valeur/b.surface_carrez),2) AS Prix_m2_3p
		FROM 
			bien b
			JOIN vente v 
				ON b.id_bien = v.id_bien
        WHERE 
			b.no_pieces = 3
			AND 
			type_local = "Appartement")
SELECT 
	Prix_m2_2p as Prix_2p,
    Prix_m2_3p as Prix_3p,
	ROUND((((prix_m2_3p/prix_m2_2p)-1)*100),2) AS 'difference en % entre apppartement avec 3 pieces et 2'
 FROM 2pieces,3pieces;
```
**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228475240-faa83421-8cef-44cf-bcfa-089817b32dfb.png)

**11. Les moyennes de valeurs foncières pour le top 3 des communes des
départements 6, 13, 33, 59 et 69.**
```sql
WITH table_pro AS (
SELECT 
	code_dep AS departement,
	nom_commune AS Commune,
	ROUND(AVG(valeur),2) AS prixmoyenne,
    RANK() OVER (PARTITION BY code_dep ORDER BY ROUND(AVG(valeur),2) DESC ) AS rang
FROM 
	bien b
	JOIN vente v
		ON b.id_bien = v.id_bien
	JOIN commune c
		ON b.id_codedep_codecommune = c.id_codedep_codecommune
WHERE c.code_dep IN ("06","13","33","59","69")
GROUP BY nom_commune, code_dep
)
SELECT 	
	departement,
	Commune,
	prixmoyenne,
    rang
FROM table_pro
WHERE rang <=3
GROUP BY departement, Commune
```

**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228475291-f8d48b99-9c1d-42bd-9b99-bf2b9a73f7b0.png)

**12.  Les 20 communes avec le plus de transactions pour 1000 habitants
pour les communes qui dépassent les 10 000 habitants.**
```sql
SELECT 
	nom_commune AS "Commune", 
    count(v.id_vente) AS "No transactions",
    ROUND((count(v.id_vente)*(1000/ptot)),2) AS "transactions par 1000 habitants"
FROM
	bien b
    JOIN vente v
		ON v.id_bien = b.id_bien
    JOIN commune c
		ON c.id_codedep_codecommune = b.id_codedep_codecommune
    JOIN population p
		ON c.id_codedep_codecommune = p.id_codedep_codecommune
WHERE p.ptot > 10000
GROUP BY nom_commune, ptot
ORDER BY ROUND((count(v.id_vente)/(ptot/1000)),2) DESC
LIMIT 20;
```

**Résultats**

![image](https://user-images.githubusercontent.com/126714469/228475351-0334e88f-89e6-49b2-9376-59ab6032fc3f.png)

