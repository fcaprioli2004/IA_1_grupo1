
; ============================================================
; Sistema experto basado exactamente en el árbol ID3 obtenido
; Compatible con CLIPS 6.x
; ============================================================


; ------------------------------------------------------------
; Plantillas
; ------------------------------------------------------------

(deftemplate estado
   (slot valor))

(deftemplate condicion
   (slot valor))

(deftemplate dosis
   (slot valor))

(deftemplate resultado
   (slot valor))


; ------------------------------------------------------------
; Funciones de entrada y validación
; ------------------------------------------------------------

(deffunction leer-estado ()
   (printout t "Estado de la enfermedad (Incipiente/Avanzado/Terminal): ")
   (bind ?v (read))

   (while
      (not
         (or
            (eq ?v Incipiente)
            (eq ?v Avanzado)
            (eq ?v Terminal)))
      do

      (printout t
         "Valor no valido. Introduzca Incipiente, Avanzado o Terminal: ")
      (bind ?v (read)))

   (return ?v))


(deffunction leer-condicion ()
   (printout t "Condicion fisica (Fuerte/Debil): ")
   (bind ?v (read))

   (while
      (not
         (or
            (eq ?v Fuerte)
            (eq ?v Debil)))
      do

      (printout t
         "Valor no valido. Introduzca Fuerte o Debil: ")
      (bind ?v (read)))

   (return ?v))


(deffunction leer-dosis ()
   (printout t "Numero de dosis: ")
   (bind ?v (read))

   (while (not (numberp ?v))
      do
      (printout t "Debe introducir un valor numerico para la dosis: ")
      (bind ?v (read)))

   (return ?v))


; ------------------------------------------------------------
; Primera pregunta: siempre es Estado, porque es la raiz ID3
; ------------------------------------------------------------

(defrule preguntar-estado
   (not (estado))
   (not (resultado))
   =>
   (bind ?e (leer-estado))
   (assert (estado (valor ?e))))


; ------------------------------------------------------------
; Rama: Estado = Avanzado
; Es una hoja pura: no se pregunta ningun otro atributo
; ------------------------------------------------------------

(defrule avanzado-curacion
   (estado (valor Avanzado))
   (not (resultado))
   =>
   (assert (resultado (valor Curacion))))


; ------------------------------------------------------------
; Rama: Estado = Terminal
; El siguiente nodo ID3 es Condicion
; ------------------------------------------------------------

(defrule preguntar-condicion-terminal
   (estado (valor Terminal))
   (not (condicion))
   (not (resultado))
   =>
   (bind ?c (leer-condicion))
   (assert (condicion (valor ?c))))


(defrule terminal-fuerte-defuncion
   (estado (valor Terminal))
   (condicion (valor Fuerte))
   (not (resultado))
   =>
   (assert (resultado (valor Defuncion))))


(defrule terminal-debil-curacion
   (estado (valor Terminal))
   (condicion (valor Debil))
   (not (resultado))
   =>
   (assert (resultado (valor Curacion))))


; ------------------------------------------------------------
; Rama: Estado = Incipiente
; El siguiente nodo ID3 es Dosis con umbral 77.5
; ------------------------------------------------------------

(defrule preguntar-dosis-incipiente
   (estado (valor Incipiente))
   (not (dosis))
   (not (resultado))
   =>
   (bind ?d (leer-dosis))
   (assert (dosis (valor ?d))))


(defrule incipiente-dosis-baja-curacion
   (estado (valor Incipiente))
   (dosis (valor ?d&:(<= ?d 77.5)))
   (not (resultado))
   =>
   (assert (resultado (valor Curacion))))


(defrule incipiente-dosis-alta-defuncion
   (estado (valor Incipiente))
   (dosis (valor ?d&:(> ?d 77.5)))
   (not (resultado))
   =>
   (assert (resultado (valor Defuncion))))


; ------------------------------------------------------------
; Mostrar un unico diagnostico y finalizar inmediatamente
; ------------------------------------------------------------

(defrule mostrar-curacion
   (resultado (valor Curacion))
   =>
   (printout t "Resultado: CURACION" crlf)
   (halt))


(defrule mostrar-defuncion
   (resultado (valor Defuncion))
   =>
   (printout t "Resultado: DEFUNCION" crlf)
   (halt))