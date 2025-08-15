import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Phone, Mail, MessageCircle, Send } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const ContactForm = ({ isOpen, onClose, contact }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    clinic_name: '',
    current_budget: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      toast({
        title: "Заявка отправлена!",
        description: "Я свяжусь с вами в течение 15 минут",
      });
      setIsSubmitting(false);
      setFormData({
        name: '',
        phone: '',
        clinic_name: '',
        current_budget: '',
        message: ''
      });
      onClose();
    }, 1000);
  };

  const handleChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-center text-gray-900">
            Получить консультацию
          </DialogTitle>
          <p className="text-center text-gray-600 mt-2">
            Обсудим ваш проект и составим план продвижения
          </p>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-sm font-medium text-gray-700">
                Ваше имя *
              </Label>
              <Input
                id="name"
                type="text"
                required
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                className="mt-1"
                placeholder="Как к вам обращаться?"
              />
            </div>

            <div>
              <Label htmlFor="phone" className="text-sm font-medium text-gray-700">
                Телефон *
              </Label>
              <Input
                id="phone"
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                className="mt-1"
                placeholder="+7 (999) 999-99-99"
              />
            </div>

            <div>
              <Label htmlFor="clinic_name" className="text-sm font-medium text-gray-700">
                Название клиники
              </Label>
              <Input
                id="clinic_name"
                type="text"
                value={formData.clinic_name}
                onChange={(e) => handleChange('clinic_name', e.target.value)}
                className="mt-1"
                placeholder="Например: Стоматология Доктор+"
              />
            </div>

            <div>
              <Label htmlFor="current_budget" className="text-sm font-medium text-gray-700">
                Текущий рекламный бюджет
              </Label>
              <Select value={formData.current_budget} onValueChange={(value) => handleChange('current_budget', value)}>
                <SelectTrigger className="mt-1">
                  <SelectValue placeholder="Выберите примерный бюджет" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">Рекламы нет</SelectItem>
                  <SelectItem value="30000">30 000 - 50 000 ₽</SelectItem>
                  <SelectItem value="50000">50 000 - 100 000 ₽</SelectItem>
                  <SelectItem value="100000">100 000 - 200 000 ₽</SelectItem>
                  <SelectItem value="200000">Более 200 000 ₽</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="message" className="text-sm font-medium text-gray-700">
                Расскажите о вашей клинике
              </Label>
              <Textarea
                id="message"
                value={formData.message}
                onChange={(e) => handleChange('message', e.target.value)}
                className="mt-1"
                placeholder="Какие услуги оказываете? Какие цели у рекламы?"
                rows={3}
              />
            </div>
          </div>

          <Button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg font-semibold"
          >
            {isSubmitting ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Отправляем...
              </div>
            ) : (
              <>
                <Send className="mr-2 h-5 w-5" />
                Получить консультацию
              </>
            )}
          </Button>

          <div className="text-center space-y-2">
            <p className="text-sm text-gray-500">
              Или свяжитесь со мной напрямую:
            </p>
            <div className="flex justify-center gap-4">
              <Button variant="outline" size="sm" className="flex items-center">
                <Phone className="mr-1 h-4 w-4" />
                Позвонить
              </Button>
              <Button variant="outline" size="sm" className="flex items-center">
                <MessageCircle className="mr-1 h-4 w-4" />
                WhatsApp
              </Button>
              <Button variant="outline" size="sm" className="flex items-center">
                <Mail className="mr-1 h-4 w-4" />
                Email
              </Button>
            </div>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default ContactForm;