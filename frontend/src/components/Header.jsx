import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Phone, Menu, X } from 'lucide-react';

const Header = ({ onOpenForm }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled 
        ? 'bg-white/95 backdrop-blur-md shadow-lg' 
        : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">E</span>
              </div>
              <span className="text-xl font-bold text-gray-900">
                Екатерина Егорова
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => scrollToSection('services')}
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Услуги
            </button>
            <button 
              onClick={() => scrollToSection('cases')}
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Кейсы
            </button>
            <button 
              onClick={() => scrollToSection('benefits')}
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Преимущества
            </button>
            <button 
              onClick={() => scrollToSection('pricing')}
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Тарифы
            </button>
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center space-x-4">
            <a 
              href="tel:+7" 
              className="flex items-center text-gray-700 hover:text-blue-600 transition-colors"
            >
              <Phone className="h-4 w-4 mr-2" />
              <span className="font-medium">+7 (XXX) XXX-XX-XX</span>
            </a>
            <Button 
              onClick={onOpenForm}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 font-medium"
            >
              Консультация
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white border-t shadow-lg">
          <div className="px-4 py-4 space-y-4">
            <button 
              onClick={() => scrollToSection('services')}
              className="block w-full text-left py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Услуги
            </button>
            <button 
              onClick={() => scrollToSection('cases')}
              className="block w-full text-left py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Кейсы
            </button>
            <button 
              onClick={() => scrollToSection('benefits')}
              className="block w-full text-left py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Преимущества
            </button>
            <button 
              onClick={() => scrollToSection('pricing')}
              className="block w-full text-left py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Тарифы
            </button>
            <div className="pt-4 border-t">
              <a 
                href="tel:+7" 
                className="flex items-center py-2 text-gray-700 hover:text-blue-600"
              >
                <Phone className="h-4 w-4 mr-2" />
                +7 (XXX) XXX-XX-XX
              </a>
              <Button 
                onClick={onOpenForm}
                className="w-full mt-2 bg-blue-600 hover:bg-blue-700 text-white"
              >
                Получить консультацию
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;