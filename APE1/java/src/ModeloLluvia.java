/** Implementa el índice de posibilidad de lluvia indicado */
public class ModeloLluvia {

    private final double[] temperaturas =
            {10, 12, 14, 16, 18, 20, 22, 24, 26, 28};

    private final double[] factores =
            {1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1};

    /** Interpola linealmente Tf para temperaturas no incluidas en la tabla. */
    public double factorTemperatura(double temperatura) {
        if (temperatura <= temperaturas[0]) return factores[0];
        if (temperatura >= temperaturas[temperaturas.length - 1])
            return factores[factores.length - 1];

        for (int i = 0; i < temperaturas.length - 1; i++) {
            if (temperatura >= temperaturas[i] && temperatura <= temperaturas[i + 1]) {
                double proporcion =
                        (temperatura - temperaturas[i])
                        / (temperaturas[i + 1] - temperaturas[i]);

                return factores[i] + proporcion * (factores[i + 1] - factores[i]);
            }
        }

        throw new IllegalArgumentException("Temperatura no válida.");
    }

    /** Clasifica I según los intervalos de la práctica. */
    public String clasificar(double indice) {
        if (indice < 0.40) return "Sin lluvia";
        if (indice < 0.60) return "Baja posibilidad";
        if (indice < 0.75) return "Lluvia probable";
        return "Lluvia";
    }

    /** Normaliza los datos y calcula I = 0.5H + 0.3N + 0.2Tf. */
    public ResultadoSimulacion evaluar(DatosMeteorologicos datos) {
        double h = datos.getHumedad() / 100.0;
        double n = datos.getNubosidad() / 100.0;
        double tf = factorTemperatura(datos.getTemperatura());
        double indice = 0.5 * h + 0.3 * n + 0.2 * tf;

        return new ResultadoSimulacion(datos, h, n, tf, indice, clasificar(indice));
    }
}