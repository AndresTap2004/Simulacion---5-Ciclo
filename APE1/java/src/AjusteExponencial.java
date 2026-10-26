import java.util.ArrayList;
import java.util.List;

/** Ajusta curvas exponenciales continuas a ambos lados del máximo observado. */
public class AjusteExponencial {

    public static class PuntoAjustado {
        private final String hora;
        private final double humedad;
        private final double nubosidad;
        private final double temperatura;
        private final double h;
        private final double n;
        private final double tf;
        private final double indiceOriginal;
        private final double indiceAjustado;
        private final String tendencia;
        private final double tasa;
        private final String estado;

        private PuntoAjustado(ResultadoSimulacion resultado,
                              double indiceAjustado, String tendencia,
                              double tasa, String estado) {
            DatosMeteorologicos datos = resultado.getDatos();
            this.hora = datos.getHora();
            this.humedad = datos.getHumedad();
            this.nubosidad = datos.getNubosidad();
            this.temperatura = datos.getTemperatura();
            this.h = resultado.getH();
            this.n = resultado.getN();
            this.tf = resultado.getTf();
            this.indiceOriginal = resultado.getIndice();
            this.indiceAjustado = indiceAjustado;
            this.tendencia = tendencia;
            this.tasa = tasa;
            this.estado = estado;
        }

        public String getHora() { return hora; }
        public double getHumedad() { return humedad; }
        public double getNubosidad() { return nubosidad; }
        public double getTemperatura() { return temperatura; }
        public double getH() { return h; }
        public double getN() { return n; }
        public double getTf() { return tf; }
        public double getIndiceOriginal() { return indiceOriginal; }
        public double getIndiceAjustado() { return indiceAjustado; }
        public String getTendencia() { return tendencia; }
        public double getTasa() { return tasa; }
        public String getEstado() { return estado; }
    }

    public static class ResultadoAjuste {
        private final List<PuntoAjustado> puntos;
        private final double p0;
        private final double tasaCrecimiento;
        private final double tasaDecrecimiento;

        private ResultadoAjuste(List<PuntoAjustado> puntos, double p0,
                                double tasaCrecimiento,
                                double tasaDecrecimiento) {
            this.puntos = puntos;
            this.p0 = p0;
            this.tasaCrecimiento = tasaCrecimiento;
            this.tasaDecrecimiento = tasaDecrecimiento;
        }

        public List<PuntoAjustado> getPuntos() { return puntos; }
        public double getP0() { return p0; }
        public double getTasaCrecimiento() { return tasaCrecimiento; }
        public double getTasaDecrecimiento() { return tasaDecrecimiento; }
    }

    public ResultadoAjuste ajustar(List<ResultadoSimulacion> resultados) {
        if (resultados.size() < 2) {
            throw new IllegalArgumentException(
                    "Se necesitan al menos dos mediciones para ajustar el modelo.");
        }

        int cantidad = resultados.size();
        double[] horas = new double[cantidad];
        double[] indices = new double[cantidad];
        int maximo = 0;

        for (int i = 0; i < cantidad; i++) {
            ResultadoSimulacion resultado = resultados.get(i);
            horas[i] = horaEnHoras(resultado.getDatos().getHora());
            indices[i] = resultado.getIndice();
            if (indices[i] <= 0) {
                throw new IllegalArgumentException(
                        "El ajuste exponencial requiere índices mayores que cero.");
            }
            if (i > 0 && horas[i] <= horas[i - 1]) {
                throw new IllegalArgumentException(
                        "Las horas deben estar ordenadas y no repetirse.");
            }
            if (indices[i] > indices[maximo]) {
                maximo = i;
            }
        }

        double p0 = indices[maximo];
        double horaMaxima = horas[maximo];
        double tasaCrecimiento = estimarTasa(
                horas, indices, 0, maximo + 1, horaMaxima, p0);
        double tasaDecrecimiento = estimarTasa(
                horas, indices, maximo, cantidad, horaMaxima, p0);

        List<PuntoAjustado> puntos = new ArrayList<>();
        ModeloLluvia modelo = new ModeloLluvia();
        for (int i = 0; i < cantidad; i++) {
            double desplazamiento = horas[i] - horaMaxima;
            String tendencia;
            double tasa;
            if (i < maximo) {
                tendencia = "Crecimiento";
                tasa = tasaCrecimiento;
            } else if (i > maximo) {
                tendencia = "Decrecimiento";
                tasa = tasaDecrecimiento;
            } else {
                tendencia = "Maximo";
                tasa = 0.0;
            }
            double indiceAjustado = p0 * Math.exp(
                    (desplazamiento <= 0 ? tasaCrecimiento : tasaDecrecimiento)
                            * desplazamiento);
            puntos.add(new PuntoAjustado(
                    resultados.get(i),
                    indiceAjustado,
                    tendencia,
                    tasa,
                    modelo.clasificar(indiceAjustado)));
        }

        return new ResultadoAjuste(
                puntos, p0, tasaCrecimiento, tasaDecrecimiento);
    }

    private static double estimarTasa(double[] horas, double[] indices,
                                      int inicio, int fin, double horaMaxima,
                                      double p0) {
        double numerador = 0.0;
        double denominador = 0.0;
        for (int i = inicio; i < fin; i++) {
            double desplazamiento = horas[i] - horaMaxima;
            numerador += desplazamiento * Math.log(indices[i] / p0);
            denominador += desplazamiento * desplazamiento;
        }
        return denominador == 0.0 ? 0.0 : numerador / denominador;
    }

    private static double horaEnHoras(String hora) {
        String[] partes = hora.split(":");
        if (partes.length != 2) {
            throw new IllegalArgumentException("Hora inválida: " + hora);
        }
        return Integer.parseInt(partes[0]) + Integer.parseInt(partes[1]) / 60.0;
    }
}
