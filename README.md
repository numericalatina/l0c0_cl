# l10n_cl_fe
Se crea este repositorio, para dar un enfoque de firma electrónica directa con el SII.

 - Se tomaron los inicios de github.com/odoo-chile/l10n_cl_dte y otros módulos de odoo-chile y la continuación de estos en github.com/dansanti/l10n_cl_dte.
 - Este repositorio se crea con la finalidad de unificar módulos y facilitar la mantención de la facturación electrónica, que se estaba muy complejo
 - Debido a que el módulo "Base report xlsx" no está publicado en la tienda desde odoo 13.0, se integra el código desde NO es necesario instalarlo https://github.com/OCA/reporting-engine
 - Se integra la consulta de datos de empresas al repositorio https://sre.cl, para permitir obtener datos digitando el rut
 - Al instalar este módulo acepta que por defecto estará activa la sincronización de datos de partners al repositorio https://sre.cl, sin embargo puede desactivarlo en todo momento desde el panel de configuración general.
 - Integración con https://apicaf.cl , Api que permite emitir folios vía api, sin pasar por la página del SII. El uso y condiciones de la api es según políticas expuestas en el sitio web mismo de la api.

 Estado:

 | Tipo Documento                | Códigos        | Envío | Consulta | Muestra Impresa | Certificación |
 |-------------------------------|----------------|-------|----------|-----------------|---------------|
 | Factura                       | FAC 33, FNA 34 |   OK  |    OK    |        OK       |       OK      |
 | Nota de Crédito               |       61       |   OK  |    OK    |        Ok       |       OK      |
 | Nota de Débito                |       56       |   OK  |    OK    |        OK       |       OK      |
 | Recepción XML Intercambio     |                |   OK  |    OK    |        OK       |       OK      |
 | Libro de Compra-Venta         |  Compra, Venta |   OK  |    OK    |        OK       |       OK      |
 | Boleta   (1)                  | BEL 39, BNA 41 |   OK  |    OK    |        OK       |       OK      |
 | Consumo de Folios Boletas (1) |                |   OK  |    OK    |        OK       |       OK      |
 | Guía de Despacho (2)          |       52       |   OK  |    OK    |        OK       |       OK      |
 | Libro de Guías (2)            |                |   OK  |    OK    |        OK       |       OK      |
 | Cesión de Créditos (3)        |                |   OK  |    OK    |        OK       |       OK      |
 | Factura Exportación (4)       |       110      |   OK  |    OK    |        OK       |       OK      |
 | Nota Crédito Exportación (4)  |       112      |   OK  |    OK    |        OK       |       OK      |
 | Nota Débito Exportación (5)   |       111      |   OK  |    OK    |        OK       |       OK      |
 | Factura de Compras (5)        |       46       |   OK  |    OK    |        OK       |       OK      |
 | Liquidación de facturas       |       43       |   X   |    X     |        X        |       OK      |

 (1) https://gitlab.com/dansanti/l10n_cl_dte_point_of_sale  
 (2) https://gitlab.com/dansanti/l10n_cl_stock_picking  
 (3) https://gitlab.com/dansanti/l10n_cl_dte_factoring  
 (4) https://gitlab.com/dansanti/l10n_cl_dte_exportacion  
 (5) NO confundir con el concepto de ingresar facturas de proveedor, que la mayoría le dice de compras, este es un documento de retención de impuestos, la recepción de documentos proveedor, está soportada, con los 4 tipos de respuesta que se deben generar según normativa del SII


  - Impuestos Soportados Para Ventas(Probados en emisión):

   A = Anticipado
   N = Normal
   R = Retención
   D = Adicional
   E = Específico

  | Código |               Nombre              |   %  | Tipo | Envío | Observación                                                                                        |
  |:------:|:---------------------------------:|:----:|:----:|:-----:|----------------------------------------------------------------------------------------------------|
  |   14   | IVA                               |  19  |   N  |   OK  |                                                                                                    |
  |   15   | IVA Retención total               |  19  |   R  |   OK  |                                                                                                    |
  |   17   | IVA al faenamiento de carnes      |   5  |   A  |   OK  |                                                                                                    |
  |   18   | IVA a las carnes                   |   5  |   A  |   OK  |                                                                                                    |
  |   19   | IVA a la Harina                   |  12  |   A  |   X   |                                                                                                    |
  |   23   | Impuesto adicional                |  15  |   N  |   X   | a) artículos oro, platino, marfil b) Joyas, piedras preciosas c) Pieles finas                      |
  |   24   | DL 825/74, ART. 42, letra b)      | 31.5 |   D  |   OK  | Licores, Piscos, whisky, aguardiente, y vinos licorosos o aromatizados.                            |
  |   25   | Vinos                             | 20.5 |   D  |   OK  |                                                                                                    |
  |   26   | Cervezas y bebidas alcohólicas    | 20.5 |   D  |   OK  |                                                                                                    |
  |   27   | Bebidas analcohólicas y minerales |  10  |   D  |   OK  |                                                                                                    |
  |   271  | Bebidas azucaradas                |  18  |   D  |   OK  | Bebidas analcohólicas y Minerales con elevado contenido de azúcares. (según indica la ley)         |
  |   28   | Impuesto especifico diesel        |      |   E  |   OK  | Compuesto                                                                                          |
  |   30   | IVA Legumbres                     |      |   R  |   X   |                                                                                                    |
  |   31   | IVA Silvestre                     |      |   R  |   X   |                                                                                                    |
  |   32   | IVA al Ganado                     |   8  |   R  |   X   |                                                                                                    |
  |   33   | IVA a la Madera                   |   8  |   R  |   X   |                                                                                                    |
  |   34   | IVA al Trigo                      |  11  |   R  |   X   |                                                                                                    |
  |   35   | Impuesto Especifico Gasolinas     |      |   E  |   OK  | Compuesto. Para  95 y 97  octanos                                                                  |
  |   36   | IVA Arroz                         |  10  |   R  |   X   |                                                                                                    |
  |   37   | IVA Hidrobiológicas               |  10  |   R  |   X   |                                                                                                    |
  |   38   | IVA Chatarras                     |  19  |   R  |   X   |                                                                                                    |
  |   39   | IVA PPA                           |  19  |   R  |   X   |                                                                                                    |
  |   41   | IVA Construcción                  |  19  |   R  |   X   | Solo factura compras                                                                               |
  |   44   | IMPUESTO art 37 Letras e, h, I, l |  15  |   A  |   X   | Tasa del 15% en 1era venta a) Alfombras, tapices b) Casa rodantes c) Caviar d) Armas de aire o gas |
  |   45   | Impuesto Pirotecnia               |  50  |   A  |   X   |                                                                                                    |
  |   46   | IVA ORO                           |  19  |   R  |   X   |                                                                                                    |
  |   47   | IVA Cartones                      |  19  |   R  |   X   |                                                                                                    |
  |   48   | IVA Frambuesas                    |  14  |   R  |       |                                                                                                    |
  |   49   | IVA factura Compra sin Retención  |   0  |   R  |   X   | hoy utilizada sólo por Bolsa de Productos de Chile, lo cual es validado por el sistema             |
  |   50   | IVA instrumentos de prepago       |  19  |   N  |   X   |                                                                                                    |
  |   51   | IVA gas natural                   |      |   E  |   X   | Compuesto                                                                                          |
  |   53   | Impuesto Suplementos              |  0.5 |   R  |   X   |                                                                                                    |

 Si tiene dudas sobre el funcionamiento y consecuencias, recordar visitar <a href="https://globalresponse.cl/forum/how-to">la documentación pública</a> o en <a href="www.sii.cl">www.sii.cl</a> o <a href="https://globalresponse.cl/helpdesk/">realizar una consulta a soporte(de pago)</a> o <a href="https://globalresponse.cl/forum/1">postear en foro(gratuito)</a>


 Agradecimientos y colaboradores:

 - Daniel Blanco
 - Nelson Ramirez
 - Carlos Toledo
 - Carlos Lopez

<a href='https://www.flow.cl/btn.php?token=ju5ulkb' target='_blank'>
  <img src='https://www.flow.cl/img/botones/btn-donar-negro.png'>
</a>
