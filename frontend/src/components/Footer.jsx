import React from 'react';
import { Button } from './ui/button';
import { Phone, Mail, MessageCircle, MapPin, Clock, ArrowUp } from 'lucide-react';

const Footer = ({ contact, onOpenForm }) => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main footer content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Company info */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">E</span>
              </div>
              <span className="text-2xl font-bold">{contact.name}</span>
            </div>
            
            <p className="text-gray-400 mb-6 text-lg leading-relaxed">
              Специализируюсь на продвижении стоматологий через контекстную рекламу. 
              Помогаю клиникам получать стабильный поток качественных заявок 
              по доступной стоимости.
            </p>
            
            <div className="space-y-3">
              <div className="flex items-center text-gray-300">
                <MapPin className="h-5 w-5 mr-3" />
                <span>Работаю с клиниками по всей России</span>
              </div>
              <div className="flex items-center text-gray-300">
                <Clock className="h-5 w-5 mr-3" />
                <span>Пн-Пт: 9:00-19:00, Сб: 10:00-16:00</span>
              </div>
            </div>
          </div>

          {/* Quick links */}
          <div>
            <h3 className="text-xl font-bold mb-6">Навигация</h3>
            <ul className="space-y-3">
              <li>
                <button 
                  onClick={() => document.getElementById('services')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Услуги
                </button>
              </li>
              <li>
                <button 
                  onClick={() => document.getElementById('cases')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Кейсы
                </button>
              </li>
              <li>
                <button 
                  onClick={() => document.getElementById('benefits')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Преимущества
                </button>
              </li>
              <li>
                <button 
                  onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Тарифы
                </button>
              </li>
            </ul>
          </div>

          {/* Contact info */}
          <div>
            <h3 className="text-xl font-bold mb-6">Контакты</h3>
            <div className="space-y-4">
              <a 
                href={`tel:${contact.phone}`}
                className="flex items-center text-gray-400 hover:text-white transition-colors group"
              >
                <Phone className="h-5 w-5 mr-3 group-hover:text-blue-400" />
                <span>{contact.phone}</span>
              </a>
              
              <a 
                href={`mailto:${contact.email}`}
                className="flex items-center text-gray-400 hover:text-white transition-colors group"
              >
                <Mail className="h-5 w-5 mr-3 group-hover:text-blue-400" />
                <span>{contact.email}</span>
              </a>
              
              <a 
                href={`https://wa.me/${contact.whatsapp}`}
                className="flex items-center text-gray-400 hover:text-white transition-colors group"
              >
                <MessageCircle className="h-5 w-5 mr-3 group-hover:text-green-400" />
                <span>WhatsApp</span>
              </a>
            </div>

            <Button 
              onClick={onOpenForm}
              className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white"
            >
              Получить консультацию
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © 2024 {contact.name}. Все права защищены.
            </div>
            
            <div className="flex items-center space-x-6">
              <button 
                className="text-gray-400 hover:text-white text-sm transition-colors"
              >
                Политика конфиденциальности
              </button>
              
              <button 
                onClick={scrollToTop}
                className="flex items-center text-gray-400 hover:text-white text-sm transition-colors group"
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