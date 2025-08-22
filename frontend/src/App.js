import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog";
import { Badge } from "./components/ui/badge";
import { Separator } from "./components/ui/separator";
import { Textarea } from "./components/ui/textarea";
import { useToast } from "./hooks/use-toast";
import { Toaster } from "./components/ui/toaster";
import { UserPlus, FileText, Users, Eye, Trash2, Edit, Download } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [clients, setClients] = useState([]);
  const [contracts, setContracts] = useState([]);
  const [selectedContract, setSelectedContract] = useState(null);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  // Client form state - simplified to 2 fields
  const [clientForm, setClientForm] = useState({
    name_or_organization: '',
    other_details: ''
  });

  // Contract form state
  const [contractForm, setContractForm] = useState({
    client_id: '',
    service_cost: '',
    service_cost_words: '',
    contract_end_date: '',
    contract_end_month: ''
  });

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось загрузить список клиентов",
        variant: "destructive",
      });
    }
  };

  const fetchContracts = async () => {
    try {
      const response = await axios.get(`${API}/contracts`);
      setContracts(response.data);
    } catch (error) {
      console.error('Error fetching contracts:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось загрузить список договоров",
        variant: "destructive",
      });
    }
  };

  useEffect(() => {
    fetchClients();
    fetchContracts();
  }, []);

  const handleClientSubmit = async (e) => {
    e.preventDefault();
    if (!clientForm.name.trim()) {
      toast({
        title: "Ошибка",
        description: "Имя клиента обязательно для заполнения",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/clients`, clientForm);
      toast({
        title: "Успешно",
        description: "Клиент добавлен",
      });
      setClientForm({
        name: '',
        organization: '',
        address: '',
        inn: '',
        phone: '',
        email: ''
      });
      fetchClients();
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось добавить клиента",
        variant: "destructive",
      });
    }
    setLoading(false);
  };

  const handleContractSubmit = async (e) => {
    e.preventDefault();
    if (!contractForm.client_id || !contractForm.service_cost || !contractForm.contract_end_date) {
      toast({
        title: "Ошибка",
        description: "Заполните все обязательные поля",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/contracts`, contractForm);
      toast({
        title: "Успешно",
        description: "Договор создан",
      });
      setContractForm({
        client_id: '',
        service_cost: '',
        service_cost_words: '',
        contract_end_date: '',
        contract_end_month: ''
      });
      fetchContracts();
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось создать договор",
        variant: "destructive",
      });
    }
    setLoading(false);
  };

  const deleteClient = async (clientId) => {
    try {
      await axios.delete(`${API}/clients/${clientId}`);
      toast({
        title: "Успешно",
        description: "Клиент удален",
      });
      fetchClients();
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось удалить клиента",
        variant: "destructive",
      });
    }
  };

  const deleteContract = async (contractId) => {
    try {
      await axios.delete(`${API}/contracts/${contractId}`);
      toast({
        title: "Успешно",
        description: "Договор удален",
      });
      fetchContracts();
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось удалить договор",
        variant: "destructive",
      });
    }
  };

  const viewContract = (contract) => {
    setSelectedContract(contract);
  };

  const downloadContract = async (contractId, clientName) => {
    try {
      const response = await axios.get(`${API}/contracts/${contractId}/download`, {
        responseType: 'blob'
      });
      
      // Create blob and download
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Договор_${clientName.replace(/\s+/g, '_')}.docx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "Успешно",
        description: "Договор скачан в формате Word",
      });
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось скачать договор",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-slate-800 mb-2 font-serif">
              Система управления договорами
            </h1>
            <p className="text-slate-600 text-lg">
              Создавайте и управляйте договорами с автоматической подстановкой данных клиента
            </p>
          </div>

          <Tabs defaultValue="clients" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="clients" className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Клиенты
              </TabsTrigger>
              <TabsTrigger value="contracts" className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Договоры
              </TabsTrigger>
              <TabsTrigger value="create-contract" className="flex items-center gap-2">
                <UserPlus className="w-4 h-4" />
                Новый договор
              </TabsTrigger>
            </TabsList>

            {/* Clients Tab */}
            <TabsContent value="clients" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-6">
                {/* Add Client Form */}
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader className="pb-4">
                    <CardTitle className="flex items-center gap-2 text-slate-800">
                      <UserPlus className="w-5 h-5 text-blue-600" />
                      Добавить клиента
                    </CardTitle>
                    <CardDescription>
                      Введите данные нового клиента для создания договоров
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleClientSubmit} className="space-y-4">
                      <div className="grid grid-cols-1 gap-4">
                        <div>
                          <Label htmlFor="name" className="text-slate-700 font-medium">
                            Имя клиента *
                          </Label>
                          <Input
                            id="name"
                            value={clientForm.name}
                            onChange={(e) => setClientForm({...clientForm, name: e.target.value})}
                            placeholder="ФИО клиента"
                            className="border-slate-200 focus:border-blue-500"
                            required
                          />
                        </div>
                        <div>
                          <Label htmlFor="organization" className="text-slate-700 font-medium">
                            Организация
                          </Label>
                          <Input
                            id="organization"
                            value={clientForm.organization}
                            onChange={(e) => setClientForm({...clientForm, organization: e.target.value})}
                            placeholder="Название организации"
                            className="border-slate-200 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <Label htmlFor="address" className="text-slate-700 font-medium">
                            Адрес
                          </Label>
                          <Textarea
                            id="address"
                            value={clientForm.address}
                            onChange={(e) => setClientForm({...clientForm, address: e.target.value})}
                            placeholder="Юридический адрес"
                            className="border-slate-200 focus:border-blue-500 resize-none"
                            rows={2}
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Label htmlFor="inn" className="text-slate-700 font-medium">
                              ИНН
                            </Label>
                            <Input
                              id="inn"
                              value={clientForm.inn}
                              onChange={(e) => setClientForm({...clientForm, inn: e.target.value})}
                              placeholder="ИНН"
                              className="border-slate-200 focus:border-blue-500"
                            />
                          </div>
                          <div>
                            <Label htmlFor="phone" className="text-slate-700 font-medium">
                              Телефон
                            </Label>
                            <Input
                              id="phone"
                              value={clientForm.phone}
                              onChange={(e) => setClientForm({...clientForm, phone: e.target.value})}
                              placeholder="+7 (XXX) XXX-XX-XX"
                              className="border-slate-200 focus:border-blue-500"
                            />
                          </div>
                        </div>
                        <div>
                          <Label htmlFor="email" className="text-slate-700 font-medium">
                            Email
                          </Label>
                          <Input
                            id="email"
                            type="email"
                            value={clientForm.email}
                            onChange={(e) => setClientForm({...clientForm, email: e.target.value})}
                            placeholder="email@example.com"
                            className="border-slate-200 focus:border-blue-500"
                          />
                        </div>
                      </div>
                      <Button 
                        type="submit" 
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5"
                      >
                        {loading ? 'Добавление...' : 'Добавить клиента'}
                      </Button>
                    </form>
                  </CardContent>
                </Card>

                {/* Clients List */}
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader className="pb-4">
                    <CardTitle className="flex items-center gap-2 text-slate-800">
                      <Users className="w-5 h-5 text-green-600" />
                      Список клиентов ({clients.length})
                    </CardTitle>
                    <CardDescription>
                      Управление существующими клиентами
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {clients.map((client) => (
                        <div key={client.id} className="p-4 border border-slate-200 rounded-lg bg-white/50 hover:bg-white/70 transition-colors">
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <h3 className="font-semibold text-slate-800">{client.name}</h3>
                              {client.organization && (
                                <p className="text-sm text-slate-600">{client.organization}</p>
                              )}
                              <div className="flex flex-wrap gap-2 mt-2">
                                {client.inn && <Badge variant="outline">ИНН: {client.inn}</Badge>}
                                {client.phone && <Badge variant="outline">{client.phone}</Badge>}
                                {client.email && <Badge variant="outline">{client.email}</Badge>}
                              </div>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => deleteClient(client.id)}
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                      {clients.length === 0 && (
                        <div className="text-center py-8 text-slate-500">
                          Нет клиентов. Добавьте первого клиента.
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Contracts Tab */}
            <TabsContent value="contracts" className="space-y-6">
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <FileText className="w-5 h-5 text-purple-600" />
                    Список договоров ({contracts.length})
                  </CardTitle>
                  <CardDescription>
                    Все созданные договоры с возможностью просмотра
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4">
                    {contracts.map((contract) => (
                      <div key={contract.id} className="p-4 border border-slate-200 rounded-lg bg-white/50 hover:bg-white/70 transition-colors">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-semibold text-slate-800">{contract.client_name}</h3>
                            <div className="flex flex-wrap gap-2 mt-2">
                              <Badge variant="outline">Стоимость: {contract.service_cost} руб/мес</Badge>
                              <Badge variant="outline">До: {contract.contract_end_date} {contract.contract_end_month} 2025</Badge>
                            </div>
                            <p className="text-sm text-slate-500 mt-2">
                              Создан: {new Date(contract.created_at).toLocaleDateString('ru-RU')}
                            </p>
                          </div>
                          <div className="flex gap-2">
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => viewContract(contract)}
                                  className="text-blue-600 border-blue-200 hover:bg-blue-50"
                                  title="Просмотр договора"
                                >
                                  <Eye className="w-4 h-4" />
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                                <DialogHeader>
                                  <DialogTitle>Договор - {contract.client_name}</DialogTitle>
                                  <DialogDescription>
                                    Предпросмотр договора об оказании услуг
                                  </DialogDescription>
                                </DialogHeader>
                                <div className="mt-4">
                                  <pre className="whitespace-pre-wrap text-sm bg-slate-50 p-4 rounded-lg border overflow-x-auto">
                                    {contract.contract_content}
                                  </pre>
                                </div>
                              </DialogContent>
                            </Dialog>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => downloadContract(contract.id, contract.client_name)}
                              className="text-green-600 border-green-200 hover:bg-green-50"
                              title="Скачать в Word"
                            >
                              <Download className="w-4 h-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => deleteContract(contract.id)}
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                              title="Удалить договор"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                    {contracts.length === 0 && (
                      <div className="text-center py-8 text-slate-500">
                        Нет договоров. Создайте первый договор.
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Create Contract Tab */}
            <TabsContent value="create-contract" className="space-y-6">
              <Card className="max-w-2xl mx-auto shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <FileText className="w-5 h-5 text-green-600" />
                    Создать новый договор
                  </CardTitle>
                  <CardDescription>
                    Выберите клиента и заполните параметры договора
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleContractSubmit} className="space-y-4">
                    <div>
                      <Label htmlFor="client_id" className="text-slate-700 font-medium">
                        Клиент *
                      </Label>
                      <select
                        id="client_id"
                        value={contractForm.client_id}
                        onChange={(e) => setContractForm({...contractForm, client_id: e.target.value})}
                        className="w-full p-2 border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none bg-white"
                        required
                      >
                        <option value="">Выберите клиента</option>
                        {clients.map((client) => (
                          <option key={client.id} value={client.id}>
                            {client.name} {client.organization && `(${client.organization})`}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="service_cost" className="text-slate-700 font-medium">
                          Стоимость услуг (цифрами) *
                        </Label>
                        <Input
                          id="service_cost"
                          value={contractForm.service_cost}
                          onChange={(e) => setContractForm({...contractForm, service_cost: e.target.value})}
                          placeholder="30000"
                          className="border-slate-200 focus:border-blue-500"
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="service_cost_words" className="text-slate-700 font-medium">
                          Стоимость прописью *
                        </Label>
                        <Input
                          id="service_cost_words"
                          value={contractForm.service_cost_words}
                          onChange={(e) => setContractForm({...contractForm, service_cost_words: e.target.value})}
                          placeholder="тридцать тысяч"
                          className="border-slate-200 focus:border-blue-500"
                          required
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="contract_end_date" className="text-slate-700 font-medium">
                          Дата окончания договора *
                        </Label>
                        <Input
                          id="contract_end_date"
                          value={contractForm.contract_end_date}
                          onChange={(e) => setContractForm({...contractForm, contract_end_date: e.target.value})}
                          placeholder="31"
                          className="border-slate-200 focus:border-blue-500"
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="contract_end_month" className="text-slate-700 font-medium">
                          Месяц окончания *
                        </Label>
                        <select
                          id="contract_end_month"
                          value={contractForm.contract_end_month}
                          onChange={(e) => setContractForm({...contractForm, contract_end_month: e.target.value})}
                          className="w-full p-2 border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none bg-white"
                          required
                        >
                          <option value="">Выберите месяц</option>
                          <option value="января">января</option>
                          <option value="февраля">февраля</option>
                          <option value="марта">марта</option>
                          <option value="апреля">апреля</option>
                          <option value="мая">мая</option>
                          <option value="июня">июня</option>
                          <option value="июля">июля</option>
                          <option value="августа">августа</option>
                          <option value="сентября">сентября</option>
                          <option value="октября">октября</option>
                          <option value="ноября">ноября</option>
                          <option value="декабря">декабря</option>
                        </select>
                      </div>
                    </div>

                    <Button 
                      type="submit" 
                      disabled={loading}
                      className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2.5"
                    >
                      {loading ? 'Создание договора...' : 'Создать договор'}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
      <Toaster />
    </div>
  );
}

export default App;