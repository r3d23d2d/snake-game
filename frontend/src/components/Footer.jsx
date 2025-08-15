import React from 'react';
import { Button } from './ui/button';
import { Phone, Mail, MessageCircle, MapPin, Clock, ArrowUp, Heart } from 'lucide-react';

const Footer = ({ contact, onOpenForm }) => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900 text-white relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 left-0 w-64 h-64 bg-cyan-500/10 rounded-full -translate-y-32 -translate-x-32 animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-80 h-80 bg-sky-600/10 rounded-full translate-y-40 translate-x-40 animate-pulse delay-1000"></div>
      
      {/* Main footer content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Company info */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-6 group">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-600 to-sky-600 rounded-lg flex items-center justify-center shadow-lg group-hover:shadow-xl group-hover:scale-110 transition-all duration-300">
                <span className="text-white font-bold">E</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-sky-400 bg-clip-text text-transparent group-hover:scale-105 transition-transform">
                {contact.name}
              </span>
            </div>
            
            <p className="text-gray-400 mb-6 text-lg leading-relaxed hover:text-gray-300 transition-colors duration-300">
              Специализируюсь на продвижении стоматологий через контекстную рекламу. 
              Помогаю клиникам получать стабильный поток качественных заявок 
              по доступной стоимости.
            </p>
            
            <div className="space-y-3">
              <div className="flex items-center text-gray-300 hover:text-cyan-400 transition-colors duration-300 group">
                <MapPin className="h-5 w-5 mr-3 group-hover:animate-bounce" />
                <span>Работаю с клиниками по всей России</span>
              </div>
              <div className="flex items-center text-gray-300 hover:text-cyan-400 transition-colors duration-300 group">
                <Clock className="h-5 w-5 mr-3 group-hover:animate-spin-slow" />
                <span>Пн-Пт: 9:00-19:00, Сб: 10:00-16:00</span>
              </div>
            </div>
          </div>

          {/* Quick links */}
          <div>
            <h3 className="text-xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-sky-400 bg-clip-text text-transparent">
              Навигация
            </h3>
            <ul className="space-y-3">
              {[
                { name: 'Услуги', id: 'services' },
                { name: 'Кейсы', id: 'cases' },
                { name: 'Преимущества', id: 'benefits' },
                { name: 'Тарифы', id: 'pricing' }
              ].map((item, index) => (
                <li key={item.id}>
                  <button 
                    onClick={() => {
                      const element = document.getElementById(item.id);
                      if (element) {
                        const offsetTop = element.offsetTop - 80;
                        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
                      }
                    }}
                    className="text-gray-400 hover:text-cyan-400 transition-all duration-300 hover:translate-x-2 hover:scale-105"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact info */}
          <div>
            <h3 className="text-xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-sky-400 bg-clip-text text-transparent">
              Контакты
            </h3>
            <div className="space-y-4">
              <a 
                href={`tel:${contact.phone}`}
                className="flex items-center text-gray-400 hover:text-cyan-400 transition-all duration-300 group hover:scale-105"
              >
                <Phone className="h-5 w-5 mr-3 group-hover:animate-bounce" />
                <span>{contact.phone}</span>
              </a>
              
              <a 
                href={`mailto:${contact.email}`}
                className="flex items-center text-gray-400 hover:text-cyan-400 transition-all duration-300 group hover:scale-105"
              >
                <Mail className="h-5 w-5 mr-3 group-hover:animate-bounce" />
                <span>{contact.email}</span>
              </a>
              
              <a 
                href={`https://wa.me/${contact.whatsapp}`}
                className="flex items-center text-gray-400 hover:text-green-400 transition-all duration-300 group hover:scale-105"
              >
                <MessageCircle className="h-5 w-5 mr-3 group-hover:animate-bounce" />
                <span>WhatsApp</span>
              </a>
            </div>

            <Button 
              onClick={onOpenForm}
              className="w-full mt-6 bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
              <span className="relative">Получить консультацию</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-800 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-gray-400 text-sm mb-4 md:mb-0 flex items-center">
              © 2024 {contact.name}. Все права защищены.
              <Heart className="w-4 h-4 mx-2 text-red-500 animate-pulse" />
              Создано с любовью
            </div>
            
            <div className="flex items-center space-x-6">
              <button 
                className="text-gray-400 hover:text-cyan-400 text-sm transition-all duration-300 hover:scale-105"
              >
                Политика конфиденциальности
              </button>
              
              <button 
                onClick={scrollToTop}
                className="flex items-center text-gray-400 hover:text-cyan-400 text-sm transition-all duration-300 group hover:scale-105"
              >
                <ArrowUp className="h-4 w-4 mr-1 group-hover:-translate-y-1 transition-transform" />
                Наверх
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;