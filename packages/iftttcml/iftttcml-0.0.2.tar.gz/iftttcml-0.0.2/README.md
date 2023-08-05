# ifttt-cml

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e8f982ceb8347b888a5d4b57d35f64b)](https://www.codacy.com/app/penicolas/ifttt-cml?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=penicolas/ifttt-cml&amp;utm_campaign=Badge_Grade)

ITFFF Custom *maker* launcher

## Descripción

Una especie de utilidad para usar el `Maker` de IFTTT y que sea fácilmente
ampliable por plugins creados en Python. PDTE EXPLICAR MÁS

## Requerimientos

 * Python3

Una cuenta en IFTTT, y al menos evento creado con `Maker`, la `key` se puede
pasar por parámetro o (mucho mejor) definir la siguiente variable de entorno:

 * `IFTTT_API_KEY`

## Instalación

```shell
git clone https://github.com/penicolas/ifttt-cml.git
cd ifttt-cml
$ pip install -e .  # desarrollo
or
$ pip install .
```

## Uso

```
usage: iftttcml [-h] [-m MAKER] [-p PARAMS] [-k KEY] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -m MAKER, --maker MAKER
                        Maker python file
  -p PARAMS, --params PARAMS
                        Params for Maker in JSON
  -k KEY, --key KEY     IFTTT API key
  -v, --version         show program's version number and exit
```

## Eventos creados ya

### metrovlc_sin_saldo

Recupera y te envía un mensaje a IFTTT usando el evento `metrovlc_sin_saldo`.

#### Uso

```
$ iftttcml --maker metrovlc_sin_saldo -p "{'bono': 3611230999, 'limite': 20}"
```

Y en tu movil aparecéra el mensaje:

```
Tarjeta 3611230999: 18.3 Euros
```
