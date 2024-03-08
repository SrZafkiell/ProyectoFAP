# Fondo de Ahorros y Prestamos ”FAP”
# (Fundamentos de programacion 2022)

-Resumen—
Este documento describe el proyecto Fondo de
Ahorros y Prestamos ”FAP” ´ de la materia de Fundamentos de
programacion (FP) — curso de la Escuela de Ingenier ´ ´ıa de
Sistemas y Computacion (EISC) de la Universidad del Valle. ´
Este proyecto academico tiene como objetivo que los estudiantes ´
demuestren las capacidades y conocimientos adquiridos durante
el transcurso del curso.

# I. INTRODUCCION´
FONDO DE AHORROS Y PRESTAMOS ”FAP” es una ´
aplicacion que permite llevar a cabo el proceso de ges- ´
tionar un fondo o tambien llamado banquito. Un una buena ´
herramienta permite estar al tanto de la situacion financiera, ´
tener controlado los socios, fechas, prestamos, ademas de ´
conocer las ganancias. .
El fondo ”FAP.es exactamente un sistema de control que
debe ser lo mas preciso posible. La tarea consiste b ´ asicamente ´
en gestionar el capital, que entra y que sale, es decir, lo que
ahorra un socio y lo que se presta.

# II. ESPECIFICACION DEL SISTEMA ´
Para de desarrollar esta aplicacion, es necesario contar con ´
un equipo de desarrollo Full Stack [1].
El equipo se conforma con m´ınimo 4 programadores y
maximo 7 programadores. ´

# II-A. Socios y ahorro
Se reune una cantidad de personas para ser socias de FAP, ´
Inicialmente hay 6 socios, sin embargo, se pueden agregar mas´
socios.
Cada socio esta en la obligaci ´ on de hacer un ahorro pro- ´
gramado cada mes (cuota fija de $25.000), pero puede ahorrar
mas si lo requiere. ´
Socio 1. ahorro $25.000 c/u
Socio 2. ahorro $50.000 c/u
Socio 3. ahorro $150.000 c/u
Socio 4. ahorro $45.000 c/u
Socio 5. ahorro $25.000 c/u
Despues de cada ahorro de cuota, se muestra un compro- ´
bante de ahorro.

# II-B. Prestamos
Con el capital ahorrado por los socios, el ADMINISTRADOR del sistema puede hacer prestamos con cuota ´
fija (numero de meses limitados) a los mismos socios ´
(1 % interes mensual) o a terceros (2.0 % o 2.5 % inter ´ es´
mensual).
Ejemplo: al senor Juan Camilo Pardo, se le hace un ˜
prestamo de COP 1.000.000 el d ´ ´ıa 22/10/2022 a 4
cuotas, con un interes de 2.5 %. Esto quiere decir que ´
el senor Juan Camilo Pardo, deber ˜ a pagar en cada mes, ´
durante 4 meses (noviembre, diciembre, enero y febrero):
$275.000.
Un prestamo que solicite un socio al numero de cuotas ´
que requiera, maximo se le prestara hasta el 90 % del ´
total ahorrado por este mismo.
Los prestamos a terceros al n ´ umero de cuotas que requie- ´
ran, pueden ser de cualquier monto que este disponible ´
en el total ahorrado del fondo.
Despues de cada pago de cuota, se muestra un compro- ´
bante de pago.

# II-C. Ganancias
La ganancia de FAP se calculan a partir de los prestamos, ´
siendo la suma de los intereses. Hay dos tipos de ganancias:
Se puede ver la ganancia actual de los prestamos (las
cuotas que ya se han pagado)
la proyeccion de la ganancia (las cuotas que se deber ´ ´ıan
pagar).

# II-D. Reportes
EL ADMINISTRADOR puede ver el monto ahorrado por
cada socio o el monto total ahorrado de todos los socios.
Los USUARIOS del sistema pueden ver si tienen un presta- ´
mo y el numero de cuotas pagadas y restantes usando su ´
nombre o su identificador
