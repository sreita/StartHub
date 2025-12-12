# --- Etapa 1: Compilación (Usamos Maven con Java 21 en Alpine) ---
FROM maven:3.9-eclipse-temurin-21-alpine AS builder
WORKDIR /app

# 1. Copiamos solo el pom.xml para aprovechar la caché de Docker
COPY pom.xml .

# 2. Descargamos dependencias (Si no cambias el pom, este paso se salta y es muy rápido)
RUN mvn dependency:go-offline

# 3. Copiamos el código fuente
COPY src ./src

# 4. Compilamos el JAR (Saltando tests para velocidad)
RUN mvn clean package -DskipTests

# --- Etapa 2: Ejecución (Imagen Ligera Java 21) ---
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Seguridad: Creamos un usuario que no sea root (Idea de Gordon, implementada en Alpine)
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copiamos el JAR compilado
COPY --from=builder /app/target/*.jar app.jar

# Optimización: Configuración de memoria automática (Idea de Gordon)
# Esto ayuda a que Java no se coma toda la RAM de tu PC
ENV JAVA_OPTS="-XX:MaxRAMPercentage=80.0"

# Puerto (Spring Boot por defecto usa 8080, pero tu config usa 8081)
# Lo alineamos a tu application.yml
EXPOSE 8081

# Comando de arranque optimizado
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]