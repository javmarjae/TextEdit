---
title: "Ejemplo"
author: "Javier Marti�nez Jaen"
date: "Febrero 2022"
output:
  html_document: default
  pdf_document: default
  word_document: default
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)  
```


## Problema 1

La base de datos `CARS2004` del paquete `PASWR2` recoge el número de coches por 1000 habitantes (`cars`), el número total de accidentes con víctimas mortales (`deaths`) y la población/1000 (`population`) para los 25 miembros de la Unión Europea en el año 2004.

1. Proporciona con `R` resumen de los datos. 
2. Utiliza la función `eda` del paquete `PASWR2` para realizar un análisis exploratorio de la variable `deaths`


### Apartado 1

```{r}
library(PASWR2)
summary(CARS2004) 
```

Como puedes observar, al compilar tu documento aparecen las sentencias de `R` y el output que te da el programa.


### Apartado 2

Ahora vamos a utilizar la función `eda` del paquete `PASWR2` para realizar un análisis exploratorio de la variable `deaths`

```{r}
eda(CARS2004$deaths)
```

En este caso, en tu documento final te aparece el código de `R`, el output numérico de la función `eda` y el output gráfico de la función `eda`.

~~~
<center style="color: green;font-size: 150%">
__Utiliza este documento para presentar las prácticas de una manera sencilla y bonita__.
</center>

~~~