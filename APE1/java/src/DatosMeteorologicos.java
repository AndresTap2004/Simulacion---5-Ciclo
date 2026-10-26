/** Representa una fila de humedad, nubosidad y temperatura por hora. */
public class DatosMeteorologicos {
    private final String hora;
    private final double humedad;
    private final double nubosidad;
    private final double temperatura;

    public DatosMeteorologicos(String hora, double humedad, double nubosidad,
                               double temperatura) {
        this.hora = hora;
        this.humedad = humedad;
        this.nubosidad = nubosidad;
        this.temperatura = temperatura;
    }

    public String getHora() { return hora; }
    public double getHumedad() { return humedad; }
    public double getNubosidad() { return nubosidad; }
    public double getTemperatura() { return temperatura; }
}