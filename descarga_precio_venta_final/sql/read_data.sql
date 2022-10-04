SELECT Nombre, link, Edad, Días from players
WHERE Precio_venta IS NULL and strftime("%Y%m%d","now") > substr(Límite, 7, 4) || "" || substr(Límite,4,2) || "" || substr(Límite, 1,2)
ORDER by Id ASC
LIMIT 500