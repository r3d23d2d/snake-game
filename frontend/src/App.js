import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Textarea } from "./components/ui/textarea";
import { useToast } from "./hooks/use-toast";
import { Toaster } from "./components/ui/toaster";
import { FileText, Eye, Edit, Download, Save, X, FileEdit } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [currentContract, setCurrentContract] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isEditingContent, setIsEditingContent] = useState(false);
  const [editedContent, setEditedContent] = useState('');
  const { toast } = useToast();

  // Contract form state
  const [contractForm, setContractForm] = useState({
    name_or_organization: '',
    other_details: '',
    service_cost: '',
    duration_months: 6
  });

  // Edit contract state
  const [editForm, setEditForm] = useState({
    name_or_organization: '',
    other_details: '',
    service_cost: '',
    duration_months: 6
  });

  // Auto-generate cost in words when service_cost changes
  const [serviceCostWords, setServiceCostWords] = useState('');

  useEffect(() => {
    if (contractForm.service_cost) {
      // This will be calculated by backend, just show placeholder
      const amount = parseInt(contractForm.service_cost);
      if (!isNaN(amount) && amount > 0) {
        setServiceCostWords('(автоматически)');
      } else {
        setServiceCostWords('');
      }
    } else {
      setServiceCostWords('');
    }
  }, [contractForm.service_cost]);

  const handleContractSubmit = async (e) => {
    e.preventDefault();
    if (!contractForm.name_or_organization.trim()) {
      toast({
        title: "Ошибка",
        description: "Имя/название организации обязательно для заполнения",
        variant: "destructive",
      });
      return;
    }

    if (!contractForm.service_cost || isNaN(parseInt(contractForm.service_cost))) {
      toast({
        title: "Ошибка", 
        description: "Введите корректную стоимость услуг",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const contractData = {
        ...contractForm,
        service_cost: parseInt(contractForm.service_cost)
      };
      
      const response = await axios.post(`${API}/contracts/direct`, contractData);
      
      toast({
        title: "Успешно",
        description: "Договор создан",
      });
      
      setCurrentContract(response.data);
      setContractForm({
        name_or_organization: '',
        other_details: '',
        service_cost: '',
        duration_months: 6
      });
    } catch (error) {
      console.error('Error creating contract:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось создать договор",
        variant: "destructive",
      });
    }
    setLoading(false);
  };

  const handleEditContract = () => {
    if (currentContract) {
      setEditForm({
        name_or_organization: currentContract.client_name,
        other_details: currentContract.client_details.includes('\n') 
          ? currentContract.client_details.split('\n').slice(1).join('\n')
          : '',
        service_cost: currentContract.service_cost.toString(),
        duration_months: calculateDurationFromDates(currentContract.contract_start_date, currentContract.contract_end_date)
      });
      setIsEditing(true);
    }
  };

  const handleEditContent = () => {
    if (currentContract) {
      setEditedContent(currentContract.contract_content);
      setIsEditingContent(true);
    }
  };

  const handleSaveContent = async () => {
    if (!editedContent.trim()) {
      toast({
        title: "Ошибка",
        description: "Содержимое договора не может быть пустым",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.put(`${API}/contracts/direct/${currentContract.id}/content`, {
        contract_content: editedContent
      });
      
      toast({
        title: "Успешно",
        description: "Содержимое договора обновлено",
      });
      
      setCurrentContract(response.data);
      setIsEditingContent(false);
    } catch (error) {
      console.error('Error updating contract content:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось обновить содержимое договора",
        variant: "destructive",
      });
    }
    setLoading(false);
  };

  const downloadCustomContract = async () => {
    if (!currentContract) return;
    
    try {
      const response = await axios.get(`${API}/contracts/direct/${currentContract.id}/download_custom`, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Договор_Редактированный_${currentContract.client_name.replace(/\s+/g, '_')}.docx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "Успешно",
        description: "Редактированный договор скачан в формате Word",
      });
    } catch (error) {
      console.error('Error downloading custom contract:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось скачать редактированный договор",
        variant: "destructive",
      });
    }
  };

  const handleSaveEdit = async () => {
    if (!editForm.name_or_organization.trim()) {
      toast({
        title: "Ошибка",
        description: "Имя/название организации обязательно для заполнения",
        variant: "destructive",
      });
      return;
    }

    if (!editForm.service_cost || isNaN(parseInt(editForm.service_cost))) {
      toast({
        title: "Ошибка",
        description: "Введите корректную стоимость услуг", 
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const contractData = {
        ...editForm,
        service_cost: parseInt(editForm.service_cost)
      };

      const response = await axios.put(`${API}/contracts/direct/${currentContract.id}`, contractData);
      
      toast({
        title: "Успешно",
        description: "Договор обновлен",
      });
      
      setCurrentContract(response.data);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating contract:', error);
      toast({
        title: "Ошибка", 
        description: "Не удалось обновить договор",
        variant: "destructive",
      });
    }
    setLoading(false);
  };

  const calculateDurationFromDates = (startDate, endDate) => {
    // Simple calculation - return 6 as default
    return 6;
  };

  const downloadContract = async () => {
    if (!currentContract) return;
    
    try {
      const response = await axios.get(`${API}/contracts/direct/${currentContract.id}/download`, {
        responseType: 'blob'
      });
      
      // Create blob and download
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Договор_${currentContract.client_name.replace(/\s+/g, '_')}.docx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "Успешно",
        description: "Договор скачан в формате Word",
      });
    } catch (error) {
      console.error('Error downloading contract:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось скачать договор",
        variant: "destructive",
      });
    }
  };

  const resetContract = () => {
    setCurrentContract(null);
    setIsEditing(false);
    setContractForm({
      name_or_organization: '',
      other_details: '',
      service_cost: '',
      duration_months: 6
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-slate-800 mb-2 font-serif">
              Создание договора об оказании услуг
            </h1>
            <p className="text-slate-600 text-lg">
              Создание и редактирование договоров об оказании услуг
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Contract Form */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-slate-800">
                  <FileText className="w-5 h-5 text-blue-600" />
                  {currentContract ? "Создать новый договор" : "Создание договора"}
                </CardTitle>
                <CardDescription>
                  {currentContract 
                    ? "Заполните данные для создания нового договора"
                    : "Заполните данные клиента и параметры договора"
                  }
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleContractSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="name_or_organization" className="text-slate-700 font-medium">
                      Имя/название организации *
                    </Label>
                    <Input
                      id="name_or_organization"
                      value={contractForm.name_or_organization}
                      onChange={(e) => setContractForm({...contractForm, name_or_organization: e.target.value})}
                      placeholder="ООО Компания или Иванов Иван Иванович"
                      className="border-slate-200 focus:border-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="other_details" className="text-slate-700 font-medium">
                      Другие данные
                    </Label>
                    <Textarea
                      id="other_details"
                      value={contractForm.other_details}
                      onChange={(e) => setContractForm({...contractForm, other_details: e.target.value})}
                      placeholder="Адрес, ИНН, телефон, email и другая информация о клиенте..."
                      className="border-slate-200 focus:border-blue-500 resize-none"
                      rows={3}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="service_cost" className="text-slate-700 font-medium">
                        Стоимость (рублей) *
                      </Label>
                      <Input
                        id="service_cost"
                        type="number"
                        value={contractForm.service_cost}
                        onChange={(e) => setContractForm({...contractForm, service_cost: e.target.value})}
                        placeholder="30000"
                        className="border-slate-200 focus:border-blue-500"
                        required
                      />
                      {serviceCostWords && (
                        <p className="text-xs text-slate-500 mt-1">
                          Прописью: {serviceCostWords}
                        </p>
                      )}
                    </div>

                    <div>
                      <Label htmlFor="duration_months" className="text-slate-700 font-medium">
                        Срок действия *
                      </Label>
                      <select
                        id="duration_months"
                        value={contractForm.duration_months}
                        onChange={(e) => setContractForm({...contractForm, duration_months: parseInt(e.target.value)})}
                        className="w-full p-2 border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none bg-white"
                        required
                      >
                        <option value={1}>1 месяц</option>
                        <option value={6}>6 месяцев</option>
                        <option value={12}>1 год</option>
                      </select>
                    </div>
                  </div>

                  <Button 
                    type="submit" 
                    disabled={loading}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5"
                  >
                    {loading ? 'Создание договора...' : 'Создать договор'}
                  </Button>

                  {currentContract && (
                    <Button 
                      type="button"
                      onClick={resetContract}
                      variant="outline"
                      className="w-full mt-2"
                    >
                      Очистить форму
                    </Button>
                  )}
                </form>
              </CardContent>
            </Card>

            {/* Contract Display */}
            {currentContract && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center gap-2 text-slate-800">
                        <FileText className="w-5 h-5 text-green-600" />
                        {currentContract.contract_number}
                      </CardTitle>
                      <CardDescription>
                        Договор создан: {new Date(currentContract.created_at).toLocaleDateString('ru-RU')}
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      {!isEditing && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={handleEditContract}
                          className="text-blue-600 border-blue-200 hover:bg-blue-50"
                          title="Редактировать"
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={downloadContract}
                        className="text-green-600 border-green-200 hover:bg-green-50"
                        title="Скачать Word"
                      >
                        <Download className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {isEditing ? (
                    <div className="space-y-4">
                      <div>
                        <Label className="text-slate-700 font-medium">
                          Имя/название организации *
                        </Label>
                        <Input
                          value={editForm.name_or_organization}
                          onChange={(e) => setEditForm({...editForm, name_or_organization: e.target.value})}
                          className="border-slate-200 focus:border-blue-500"
                        />
                      </div>

                      <div>
                        <Label className="text-slate-700 font-medium">
                          Другие данные
                        </Label>
                        <Textarea
                          value={editForm.other_details}
                          onChange={(e) => setEditForm({...editForm, other_details: e.target.value})}
                          className="border-slate-200 focus:border-blue-500 resize-none"
                          rows={2}
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label className="text-slate-700 font-medium">
                            Стоимость (рублей) *
                          </Label>
                          <Input
                            type="number"
                            value={editForm.service_cost}
                            onChange={(e) => setEditForm({...editForm, service_cost: e.target.value})}
                            className="border-slate-200 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <Label className="text-slate-700 font-medium">
                            Срок действия *
                          </Label>
                          <select
                            value={editForm.duration_months}
                            onChange={(e) => setEditForm({...editForm, duration_months: parseInt(e.target.value)})}
                            className="w-full p-2 border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none bg-white"
                          >
                            <option value={1}>1 месяц</option>
                            <option value={6}>6 месяцев</option>
                            <option value={12}>1 год</option>
                          </select>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          onClick={handleSaveEdit}
                          disabled={loading}
                          className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                        >
                          <Save className="w-4 h-4 mr-2" />
                          {loading ? 'Сохранение...' : 'Сохранить'}
                        </Button>
                        <Button
                          onClick={() => setIsEditing(false)}
                          variant="outline"
                          className="flex-1"
                        >
                          <X className="w-4 h-4 mr-2" />
                          Отмена
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-semibold text-slate-800 mb-2">Информация о клиенте:</h3>
                        <div className="bg-slate-50 p-3 rounded-lg">
                          <p className="font-medium">{currentContract.client_name}</p>
                          {currentContract.client_details.includes('\n') && (
                            <p className="text-sm text-slate-600 mt-1 whitespace-pre-wrap">
                              {currentContract.client_details.split('\n').slice(1).join('\n')}
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-slate-600">Стоимость:</p>
                          <p className="font-semibold">{currentContract.service_cost.toLocaleString()} руб/мес</p>
                          <p className="text-xs text-slate-500">({currentContract.service_cost_words})</p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-600">Срок действия:</p>
                          <p className="font-semibold">
                            До {currentContract.contract_end_date} {currentContract.contract_end_month} {currentContract.contract_end_year || '2025'}
                          </p>
                        </div>
                      </div>

                      <details className="mt-4">
                        <summary className="cursor-pointer text-sm font-medium text-slate-700 hover:text-slate-900">
                          Просмотр текста договора
                        </summary>
                        <div className="mt-2 max-h-96 overflow-y-auto">
                          <pre className="whitespace-pre-wrap text-xs bg-slate-50 p-3 rounded-lg border">
                            {currentContract.contract_content}
                          </pre>
                        </div>
                      </details>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Initial state when no contract */}
            {!currentContract && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm flex items-center justify-center">
                <CardContent className="text-center py-12">
                  <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-600 mb-2">
                    Договор не создан
                  </h3>
                  <p className="text-slate-500">
                    Заполните форму слева и нажмите "Создать договор"<br />
                    для автоматической генерации договора
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
      <Toaster />
    </div>
  );
}

export default App;