# document_series (Odoo 19 Community)

1. Copiar la carpeta `document_series` a tu ruta de addons.
2. Reiniciar Odoo, actualizar lista de aplicaciones e instalar "Series de documentos".
3. Contabilidad > Configuración > Series de documentos: crear F001, B001, T001, etc.
4. Vincular cada serie a su diario (recomendado: un diario por serie).

Nota: probar primero en una base de pruebas. account.move valida el formato
del nombre contra el diario; si hay conflicto, revisar sequence_mixin.py.
