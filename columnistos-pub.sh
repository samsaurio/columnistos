#!/bin/bash
# Script que hace lo siguiente: 
#   1. Saca los resultados
#   2. Los expone como CSV en pub
#   3. Los expone como sqlite pub
#   OBS: Mantiene un solo archvo que se sobreescribe cada ejecución

# Variables
pais="$1"
carpetascript="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
carpeta="$carpetascript"/public
bincompose=/usr/local/bin/docker-compose

# Controlo que se ingrese al menos 1 parametro
nom_script="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
if [ $# -lt 1 ]; then
    echo -e "\nModo de empleo: $nom_script [país]"
    echo -e "\n  utilice código ISO: py | uy | ar\n"
    exit 1
fi

# Funciones
function obtengoCsv {

  # Creo carpeta
  mkdir -p $carpeta
  # Obtengo resultados
  # NOTICE: como la base ahora no diferencia país, el código país solo se pide
  #        para nombrar al archivo csv
  echo -e "Obteniendo resultados y guardando en $carpeta"
  $bincompose -f $carpetascript/docker-compose.yml run --rm app sqlite3 \
	-header -csv /usr/src/app/diarios/diarios.sqlite \
	"select * from articles a join authors aut where a.author_id = aut.id;" > \
	"$carpeta"/"$pais"_articulos.csv || exit 1
}

function obtengoSqlite {
  mkdir -p $carpeta
  echo -e "Obteniendo resultados y guardando en $carpeta"
  cp "$carpetascript/diarios/diarios.sqlite" "$carpeta"/"$pais"_columnistos.sqlite || exit 1
}

#######################
# Programa principal
#######################

#FIXME: controlar que el código país sea correcto
#controlarCod

#FIXME: controlar errores en ambas
obtengoCsv

obtengoSqlite

# Si pasó las dos funciones no hubo error
# FIXME: esto se podría hacer mejor
echo -e "Generando registro en $carpeta"
echo "$(date +%Y%m%d)" > "$carpeta"/"$pais"_log.txt
