SELECT Nombre, link, Edad, Días from players
WHERE Precio_venta IS NULL and (Límite = substr(Límite, 7) || "" || substr(Límite,4,2) || "" || substr(Límite, 1,2)) < strftime("%Y%m%d","now")
ORDER by Id ASC
LIMIT 400