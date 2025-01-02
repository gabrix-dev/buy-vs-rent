import numpy_financial as npf
import matplotlib.pyplot as plt

# --- Configuración de parámetros ajustables ---
precio_vivienda = 300000  # Precio de la vivienda en euros
pago_inicial = 60000  # Pago inicial (entrada) de la hipoteca
interes_hipoteca = 0.03  # Tasa de interés fija anual de la hipoteca (3%)
plazo_hipoteca = 30  # Plazo de la hipoteca en años
precio_alquiler = 1000  # Precio del alquiler mensual
revalorizacion_anual_vivienda = (
    0.02  # Revalorización anual esperada de la vivienda (2%)
)
rentabilidad_sp500 = 0.07  # Rentabilidad anual esperada del S&P500 (7%)
inflacion = 0.02  # Inflación anual esperada (2%)

# --- Cálculos de hipoteca ---
prestamo = precio_vivienda - pago_inicial
n_meses = plazo_hipoteca * 12
cuota_mensual = npf.pmt(interes_hipoteca / 12, n_meses, -prestamo)

# --- Simulación de 30 años ---
valor_vivienda = precio_vivienda
inversion_sp500 = pago_inicial
valor_portfolio_sp500 = pago_inicial

hipoteca_total_pagada = 0
alquiler_total_pagado = 0

log = []

for year in range(plazo_hipoteca):
    for month in range(12):
        # Pagos de hipoteca
        hipoteca_total_pagada += cuota_mensual
        # Inversión en S&P500 (lo que no se va en alquiler)
        ahorro_mensual = cuota_mensual - precio_alquiler
        if ahorro_mensual > 0:
            valor_portfolio_sp500 += ahorro_mensual
            inversion_sp500 += ahorro_mensual
        alquiler_total_pagado += precio_alquiler

    # Revalorización anual
    valor_vivienda *= 1 + revalorizacion_anual_vivienda
    valor_portfolio_sp500 *= 1 + rentabilidad_sp500
    precio_alquiler *= 1 + inflacion

    log.append(
        f"Año {year + 1}: Valor vivienda: {valor_vivienda:.2f} €, Valor S&P500: {valor_portfolio_sp500:.2f} €"
    )

# --- Resultados finales ---
valor_neto_vivienda = valor_vivienda - hipoteca_total_pagada
valor_neto_sp500 = valor_portfolio_sp500

log.append("\n--- Resumen Final ---")
log.append(f"Valor final de la vivienda: {valor_vivienda:.2f} €")
log.append(f"Hipoteca total pagada: {hipoteca_total_pagada:.2f} €")
log.append(f"Valor neto de la vivienda: {valor_neto_vivienda:.2f} €")
log.append(f"Valor total del portfolio S&P500: {valor_neto_sp500:.2f} €")
log.append(f"Total pagado en alquiler: {alquiler_total_pagado:.2f} €")

print("\n".join(log))

# --- Visualización de resultados ---
plt.figure(figsize=(10, 6))
plt.plot(
    range(1, plazo_hipoteca + 1),
    [
        precio_vivienda * (1 + revalorizacion_anual_vivienda) ** i
        for i in range(plazo_hipoteca)
    ],
    label="Valor Vivienda",
)
plt.plot(
    range(1, plazo_hipoteca + 1),
    [pago_inicial * (1 + rentabilidad_sp500) ** i for i in range(plazo_hipoteca)],
    label="Valor S&P500",
)
plt.xlabel("Años")
plt.ylabel("Valor (€)")
plt.title("Comparativa: Compra de vivienda vs Inversión en S&P500")
plt.legend()
plt.grid(True)
plt.show()
