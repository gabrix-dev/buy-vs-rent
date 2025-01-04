import matplotlib.pyplot as plt
import numpy_financial as npf

# Costes de compra de una vivienda
precio_vivienda = 300000
pago_inicial_casa = precio_vivienda * 0.2
tasacion_notaría_y_otros = 0.08 * precio_vivienda

pago_inicial_total = pago_inicial_casa + tasacion_notaría_y_otros
print(f"Pago inicial de propiedad total: {pago_inicial_total:.2f} €")

# Costes de propiedad
valor_catastral = 0.45 * precio_vivienda
impuesto_ibi_mensual = 0.66 / 100 * valor_catastral / 12
porcentaje_gasto_mantenimiento = 0.01
gasto_mantenimiento_mensual = porcentaje_gasto_mantenimiento * precio_vivienda / 12
gastos_comunidad_mensual = 50
poliza_seguro_hogar_mensual = 250 / 12
tasa_basuras_mensual = 100 / 12
costes_propiedad_mensual = (
    gasto_mantenimiento_mensual
    + impuesto_ibi_mensual
    + gastos_comunidad_mensual
    + poliza_seguro_hogar_mensual
    + tasa_basuras_mensual
)

# Costes hipoteca
interes_hipoteca = 0.02
plazo_hipoteca = 25
prestamo = precio_vivienda - pago_inicial_casa
n_meses = plazo_hipoteca * 12
cuota_mensual = npf.pmt(interes_hipoteca / 12, n_meses, -prestamo)

coste_mensual_total = cuota_mensual + costes_propiedad_mensual
print(f"Coste mensual de propiedad total: {coste_mensual_total:.2f} €")

# Parametros de analisis de la inversión
revalorizacion_anual_vivienda = 0.02
rentabilidad_anual_sp500 = 0.07
rentabilidad_anual_real_sp500 = rentabilidad_anual_sp500 - 0.02
subida_alquiler_anual = 0.01
precio_alquiler = 1000
inversion_mensual_sp500 = coste_mensual_total - precio_alquiler
print(f"Inversion en S&P500 mensual: {inversion_mensual_sp500:.2f} €")

valor_vivienda = precio_vivienda
inversion_sp500 = pago_inicial_total
valor_portfolio_sp500 = pago_inicial_total
propiedad_total_pagado = 0
alquiler_total_pagado = 0

log = []
valores_vivienda = []
valores_sp500 = []

for year in range(plazo_hipoteca):
    for month in range(12):
        propiedad_total_pagado += coste_mensual_total
        if inversion_mensual_sp500 > 0:
            valor_portfolio_sp500 += inversion_mensual_sp500
            inversion_sp500 += inversion_mensual_sp500
        alquiler_total_pagado += precio_alquiler

    # Revalorización anual
    valor_vivienda *= 1 + revalorizacion_anual_vivienda
    valor_portfolio_sp500 *= 1 + rentabilidad_anual_real_sp500
    precio_alquiler *= 1 + subida_alquiler_anual

    valores_vivienda.append(valor_vivienda)
    valores_sp500.append(valor_portfolio_sp500)

    log.append(
        f"Año {year + 1}: Valor vivienda: {valor_vivienda:.2f} €, Valor S&P500: {valor_portfolio_sp500:.2f} €"
    )

# --- Resultados finales ---
log.append("\n--- Resumen Final ---")
log.append(f"Valor final de la vivienda: {valor_vivienda:.2f} €")
log.append(f"Valor final del portfolio S&P500: {valor_portfolio_sp500:.2f} €")
log.append(
    f"Valor líquido final del portfolio S&P500: {valor_portfolio_sp500*(1-0.28):.2f} €"
)
log.append(f"Hipoteca total pagada: {propiedad_total_pagado:.2f} €")
log.append(f"Total pagado en alquiler: {alquiler_total_pagado:.2f} €")
log.append(f"Total invertido en S&P500: {inversion_sp500:.2f} €")

print("\n".join(log))

# --- Gráficas ---
plt.figure(figsize=(10, 6))
plt.plot(range(1, plazo_hipoteca + 1), valores_vivienda, label="Valor Vivienda")
plt.plot(range(1, plazo_hipoteca + 1), valores_sp500, label="Valor Portfolio S&P500")
plt.xlabel("Años")
plt.ylabel("Valor (€)")
plt.title("Evolución anual: Valor de Vivienda vs S&P500")
plt.legend()
plt.grid(True)
plt.show()
