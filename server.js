import express from "express";
import cors from "cors";
import path from "path";
import fs from "fs";
import multer from "multer";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const upload = multer({ dest: "uploads/" });

const app = express();
app.use(cors());
app.use(express.json());

// frontend
app.use(express.static(path.join(__dirname, "frontend")));

// API correta
app.get("/api/pontos", (req, res) => {
  const filePath = path.join(__dirname, "pontos.json");

  if (!fs.existsSync(filePath)) {
    return res.json([]);
  }

  const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
  res.json(data);
});

app.get("/api/melhor-ponto", (req, res) => {
  const filePath = path.join(__dirname, "melhor_ponto.json");

  if (!fs.existsSync(filePath)) {
    return res.status(404).json(null);
  }

  const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
  res.json(data);
});

app.post("/api/upload", upload.single("arquivo"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ mensagem: "Nenhum arquivo enviado" });
  }

  // Aqui depois chamaremos o Python
  console.log("Arquivo recebido:", req.file.originalname);

  res.json({
    mensagem: "Planilha importada com sucesso. Processando endereços..."
  });
});


app.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});
