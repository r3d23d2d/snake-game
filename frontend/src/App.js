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
      // Filename will be set by backend Content-Disposition header
      link.download = `Договор для ${currentContract.client_name} (редактированный).docx`;
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
      // Filename will be set by backend Content-Disposition header
      link.download = `Договор для ${currentContract.client_name}.docx`;
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
    setIsEditingContent(false);
    setEditedContent('');
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
        <div className="max-w-4xl mx-auto">
          
          {/* If no contract exists, show form */}
          {!currentContract && (
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-slate-800">
                  <FileText className="w-5 h-5 text-blue-600" />
                  Создание договора
                </CardTitle>
                <CardDescription>
                  Заполните данные клиента и параметры договора
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
                </form>
              </CardContent>
            </Card>
          )}

          {/* If contract exists, show simplified view */}
          {currentContract && (
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardContent className="p-8">
                {isEditingContent ? (
                  <div className="space-y-4">
                    <div>
                      <Label className="text-slate-700 font-medium mb-2 block">
                        Редактирование текста договора
                      </Label>
                      <Textarea
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        className="border-slate-200 focus:border-purple-500 resize-none min-h-[400px] font-mono text-sm"
                        placeholder="Введите текст договора..."
                      />
                    </div>

                    <div className="flex gap-2">
                      <Button
                        onClick={handleSaveContent}
                        disabled={loading}
                        className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
                      >
                        <Save className="w-4 h-4 mr-2" />
                        {loading ? 'Сохранение...' : 'Сохранить изменения'}
                      </Button>
                      <Button
                        onClick={() => setIsEditingContent(false)}
                        variant="outline"
                        className="flex-1"
                      >
                        <X className="w-4 h-4 mr-2" />
                        Отмена
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="text-center space-y-6">
                    <h1 className="text-2xl font-bold text-slate-800">
                      Договор об оказании услуг для {currentContract.client_name}
                    </h1>
                    
                    <div className="flex justify-center gap-4">
                      <Button
                        onClick={handleEditContent}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2"
                      >
                        Редактировать
                      </Button>
                      <Button
                        onClick={downloadContract}
                        className="bg-green-600 hover:bg-green-700 text-white px-6 py-2"
                      >
                        Скачать Word
                      </Button>
                    </div>
                    
                    <Button 
                      onClick={resetContract}
                      variant="outline"
                      className="mt-4"
                    >
                      Создать новый договор
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
      <Toaster />
    </div>
  );
}

export default App;