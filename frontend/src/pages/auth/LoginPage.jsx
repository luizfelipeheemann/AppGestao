import { useState } from "react";
import { Eye, EyeOff, User, Lock, LogIn, UserPlus } from "lucide-react"; // ===== ADICIONADO: UserPlus =====
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
// ===== ADICIONADO: Import do Tabs =====
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// ===== FIM DA ADIÇÃO =====
import { useAuth } from "../../contexts/AuthContext";
import LoadingSpinner from "../../components/LoadingSpinner";

export default function LoginPage() {
  const { login } = useAuth();

  // Estados para LOGIN
  const initialEmail = import.meta.env.VITE_DEV_USER_EMAIL || "";
  const initialPassword = import.meta.env.VITE_DEV_USER_PASSWORD || "";
  const [email, setEmail] = useState(initialEmail);
  const [senha, setSenha] = useState(initialPassword);

  // ===== ADICIONADO: Estados para CADASTRO =====
  const [registerData, setRegisterData] = useState({
    nome: "",
    email: "",
    senha: "",
    confirmarSenha: ""
  });
  // ===== FIM DA ADIÇÃO =====

  const [showPassword, setShowPassword] = useState(false);
  // ===== ADICIONADO: Estado para mostrar senha do cadastro =====
  const [showRegisterPassword, setShowRegisterPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  // ===== FIM DA ADIÇÃO =====
  
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  // ===== ADICIONADO: Estado para sucesso do cadastro =====
  const [successMsg, setSuccessMsg] = useState("");
  // ===== FIM DA ADIÇÃO =====

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");
    const result = await login(email, senha);
    setLoading(false);
    if (!result.success) {
      setErrorMsg(result.error || "Não foi possível fazer login.");
    }
  };

  // ===== ADICIONADO: Função para cadastro =====
  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");
    setSuccessMsg("");

    // Validações básicas
    if (registerData.senha !== registerData.confirmarSenha) {
      setErrorMsg("As senhas não coincidem");
      setLoading(false);
      return;
    }

    if (registerData.senha.length < 6) {
      setErrorMsg("A senha deve ter pelo menos 6 caracteres");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nome: registerData.nome,
          email: registerData.email,
          senha: registerData.senha,
          confirmar_senha: registerData.confirmarSenha
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMsg("Usuário criado com sucesso! Faça login para continuar.");
        setRegisterData({ nome: "", email: "", senha: "", confirmarSenha: "" });
        // Opcional: mudar para aba de login automaticamente
        setTimeout(() => {
          const loginTab = document.querySelector('[value="login"]');
          if (loginTab) loginTab.click();
        }, 2000);
      } else {
        setErrorMsg(data.detail || "Erro ao criar usuário");
      }
    } catch (error) {
      setErrorMsg("Erro de conexão. Tente novamente.");
    }

    setLoading(false);
  };

  const handleRegisterInputChange = (field, value) => {
    setRegisterData(prev => ({
      ...prev,
      [field]: value
    }));
  };
  // ===== FIM DA ADIÇÃO =====

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="w-full max-w-md">
        <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <User className="h-8 w-8 text-primary" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold">
              Sistema de Gestão
            </CardTitle>
            <CardDescription>
              {/* ===== MODIFICADO: Descrição dinâmica ===== */}
              Entre com suas credenciais ou crie uma nova conta
              {/* ===== FIM DA MODIFICAÇÃO ===== */}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* ===== ADICIONADO: Tabs para Login/Cadastro ===== */}
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Login</TabsTrigger>
                <TabsTrigger value="register">Cadastro</TabsTrigger>
              </TabsList>
              
              {/* TAB DE LOGIN */}
              <TabsContent value="login">
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="seu@email.com"
                        className="pl-10"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="senha">Senha</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="senha"
                        type={showPassword ? "text" : "password"}
                        value={senha}
                        onChange={(e) => setSenha(e.target.value)}
                        placeholder="Sua senha"
                        className="pl-10 pr-10"
                        required
                        disabled={loading}
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setShowPassword(!showPassword)}
                        disabled={loading}
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4 text-muted-foreground" />
                        ) : (
                          <Eye className="h-4 w-4 text-muted-foreground" />
                        )}
                      </Button>
                    </div>
                  </div>

                  {errorMsg && (
                    <p className="text-sm text-red-600 text-center">{errorMsg}</p>
                  )}

                  <Button
                    type="submit"
                    className="w-full"
                    disabled={loading || !email || !senha}
                  >
                    {loading ? (
                      <LoadingSpinner size="small" text="" />
                    ) : (
                      <>
                        <LogIn className="mr-2 h-4 w-4" />
                        Entrar
                      </>
                    )}
                  </Button>
                </form>
              </TabsContent>

              {/* TAB DE CADASTRO */}
              <TabsContent value="register">
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="register-nome">Nome Completo</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="register-nome"
                        type="text"
                        value={registerData.nome}
                        onChange={(e) => handleRegisterInputChange("nome", e.target.value)}
                        placeholder="Seu nome completo"
                        className="pl-10"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="register-email">Email</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="register-email"
                        type="email"
                        value={registerData.email}
                        onChange={(e) => handleRegisterInputChange("email", e.target.value)}
                        placeholder="seu@email.com"
                        className="pl-10"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="register-senha">Senha</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="register-senha"
                        type={showRegisterPassword ? "text" : "password"}
                        value={registerData.senha}
                        onChange={(e) => handleRegisterInputChange("senha", e.target.value)}
                        placeholder="Mínimo 6 caracteres"
                        className="pl-10 pr-10"
                        required
                        disabled={loading}
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setShowRegisterPassword(!showRegisterPassword)}
                        disabled={loading}
                      >
                        {showRegisterPassword ? (
                          <EyeOff className="h-4 w-4 text-muted-foreground" />
                        ) : (
                          <Eye className="h-4 w-4 text-muted-foreground" />
                        )}
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="register-confirmar-senha">Confirmar Senha</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="register-confirmar-senha"
                        type={showConfirmPassword ? "text" : "password"}
                        value={registerData.confirmarSenha}
                        onChange={(e) => handleRegisterInputChange("confirmarSenha", e.target.value)}
                        placeholder="Confirme sua senha"
                        className="pl-10 pr-10"
                        required
                        disabled={loading}
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        disabled={loading}
                      >
                        {showConfirmPassword ? (
                          <EyeOff className="h-4 w-4 text-muted-foreground" />
                        ) : (
                          <Eye className="h-4 w-4 text-muted-foreground" />
                        )}
                      </Button>
                    </div>
                  </div>

                  {errorMsg && (
                    <p className="text-sm text-red-600 text-center">{errorMsg}</p>
                  )}
                  
                  {successMsg && (
                    <p className="text-sm text-green-600 text-center">{successMsg}</p>
                  )}

                  <Button
                    type="submit"
                    className="w-full"
                    disabled={loading || !registerData.nome || !registerData.email || !registerData.senha || !registerData.confirmarSenha}
                  >
                    {loading ? (
                      <LoadingSpinner size="small" text="" />
                    ) : (
                      <>
                        <UserPlus className="mr-2 h-4 w-4" />
                        Criar Conta
                      </>
                    )}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
            {/* ===== FIM DA ADIÇÃO ===== */}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

