/** Resultados del modelo para una fila de datos meteorológicos. */
public class ResultadoSimulacion {
    private final DatosMeteorologicos datos;
    private final double h;
    private final double n;
    private final double tf;
    private final double indice;
    private final String estado;

    public ResultadoSimulacion(DatosMeteorologicos datos, double h, double n,
                               double tf, double indice, String estado) {
        this.datos = datos;
        this.h = h;
        this.n = n;
        this.tf = tf;
        this.indice = indice;
        this.estado = estado;
    }

    public DatosMeteorologicos getDatos() { return datos; }
    public double getH() { return h; }
    public double getN() { return n; }
    public double getTf() { return tf; }
    public double getIndice() { return indice; }
    public String getEstado() { return estado; }
}