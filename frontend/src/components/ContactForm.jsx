import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Phone, Mail, MessageCircle, Send, Sparkles, CheckCircle } from 'lucide-react';
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
    
    // Simulate form submission with animation
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
    }, 1500);
  };

  const handleChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md bg-white/95 backdrop-blur-sm border-0 shadow-2xl" aria-describedby="dialog-description">
        <DialogHeader className="text-center">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-cyan-100 to-sky-200 rounded-full flex items-center justify-center mb-4 animate-bounce">
            <Sparkles className="w-8 h-8 text-cyan-600" />
          </div>
          <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent">
            Получить консультацию
          </DialogTitle>
          <p id="dialog-description" className="text-gray-600 mt-2">
            Обсудим ваш проект и составим план продвижения
          </p>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in-up">
          <div className="space-y-4">
            <div className="animate-fade-in-up delay-100">
              <Label htmlFor="name" className="text-sm font-medium text-gray-700 flex items-center">
                Ваше имя *
              </Label>
              <Input
                id="name"
                type="text"
                required
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                className="mt-1 border-cyan-200 focus:border-cyan-500 focus:ring-cyan-500 transition-all duration-300"
                placeholder="Как к вам обращаться?"
              />
            </div>

            <div className="animate-fade-in-up delay-200">
              <Label htmlFor="phone" className="text-sm font-medium text-gray-700">
                Телефон *
              </Label>
              <Input
                id="phone"
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                className="mt-1 border-cyan-200 focus:border-cyan-500 focus:ring-cyan-500 transition-all duration-300"
                placeholder="+7 (999) 999-99-99"
              />
            </div>

            <div className="animate-fade-in-up delay-300">
              <Label htmlFor="clinic_name" className="text-sm font-medium text-gray-700">
                Название клиники
              </Label>
              <Input
                id="clinic_name"
                type="text"
                value={formData.clinic_name}
                onChange={(e) => handleChange('clinic_name', e.target.value)}
                className="mt-1 border-cyan-200 focus:border-cyan-500 focus:ring-cyan-500 transition-all duration-300"
                placeholder="Например: Стоматология Доктор+"
              />
            </div>

            <div className="animate-fade-in-up delay-400">
              <Label htmlFor="current_budget" className="text-sm font-medium text-gray-700">
                Текущий рекламный бюджет
              </Label>
              <Select value={formData.current_budget} onValueChange={(value) => handleChange('current_budget', value)}>
                <SelectTrigger className="mt-1 border-cyan-200 focus:border-cyan-500 focus:ring-cyan-500 transition-all duration-300">
                  <SelectValue placeholder="Выберите примерный бюджет" />
                </SelectTrigger>
                <SelectContent className="bg-white/95 backdrop-blur-md border-cyan-200">
                  <SelectItem value="0" className="hover:bg-cyan-50">Рекламы нет</SelectItem>
                  <SelectItem value="30000" className="hover:bg-cyan-50">30 000 - 50 000 ₽</SelectItem>
                  <SelectItem value="50000" className="hover:bg-cyan-50">50 000 - 100 000 ₽</SelectItem>
                  <SelectItem value="100000" className="hover:bg-cyan-50">100 000 - 200 000 ₽</SelectItem>
                  <SelectItem value="200000" className="hover:bg-cyan-50">Более 200 000 ₽</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="animate-fade-in-up delay-500">
              <Label htmlFor="message" className="text-sm font-medium text-gray-700">
                Расскажите о вашей клинике
              </Label>
              <Textarea
                id="message"
                value={formData.message}
                onChange={(e) => handleChange('message', e.target.value)}
                className="mt-1 border-cyan-200 focus:border-cyan-500 focus:ring-cyan-500 transition-all duration-300 resize-none"
                placeholder="Какие услуги оказываете? Какие цели у рекламы?"
                rows={3}
              />
            </div>
          </div>

          <Button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white py-3 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 relative overflow-hidden group animate-fade-in-up delay-600"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
            {isSubmitting ? (
              <div className="flex items-center relative">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Отправляем...
              </div>
            ) : (
              <div className="flex items-center relative">
                <Send className="mr-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                Получить консультацию
              </div>
            )}
          </Button>

          <div className="text-center space-y-3 animate-fade-in-up delay-700">
            <div className="flex items-center justify-center space-x-2 text-cyan-600 bg-cyan-50 rounded-lg p-2">
              <CheckCircle className="w-4 h-4" />
              <span className="text-sm font-medium">Ответим в течение 15 минут</span>
            </div>
            
            <p className="text-sm text-gray-500">
              Или свяжитесь со мной напрямую:
            </p>
            <div className="flex justify-center gap-3">
              <Button variant="outline" size="sm" className="flex items-center border-cyan-200 hover:border-cyan-500 hover:bg-cyan-50 transition-all duration-300 hover:scale-105">
                <Phone className="mr-1 h-4 w-4 text-cyan-600" />
                Позвонить
              </Button>
              <Button variant="outline" size="sm" className="flex items-center border-cyan-200 hover:border-green-500 hover:bg-green-50 transition-all duration-300 hover:scale-105">
                <MessageCircle className="mr-1 h-4 w-4 text-green-600" />
                WhatsApp
              </Button>
              <Button variant="outline" size="sm" className="flex items-center border-cyan-200 hover:border-blue-500 hover:bg-blue-50 transition-all duration-300 hover:scale-105">
                <Mail className="mr-1 h-4 w-4 text-blue-600" />
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