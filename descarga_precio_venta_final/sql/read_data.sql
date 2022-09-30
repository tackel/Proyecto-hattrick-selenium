SELECT Nombre, link, Edad, Días from players
WHERE Precio_venta IS NULL and Límite < strftime("%d %m %Y","now")
ORDER by Id ASC
LIMIT 400