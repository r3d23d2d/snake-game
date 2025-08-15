import React from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { ArrowRight, Phone, MessageCircle, Sparkles, TrendingUp } from 'lucide-react';

const Hero = ({ data, onOpenForm }) => {
  return (
    <section className="relative min-h-screen bg-gradient-to-br from-cyan-50 via-white to-sky-50 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-200/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-sky-300/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
        <div className="absolute -bottom-8 left-20 w-80 h-80 bg-cyan-300/25 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-2000"></div>
      </div>
      
      {/* Floating particles */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-300"></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-sky-500 rounded-full animate-bounce delay-700"></div>
        <div className="absolute bottom-1/4 left-1/3 w-3 h-3 bg-cyan-300 rounded-full animate-bounce delay-1000"></div>
        <div className="absolute top-1/2 right-1/4 w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce delay-1500"></div>
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        <div className="grid lg:grid-cols-2 gap-12 items-center min-h-[80vh]">
          {/* Left content */}
          <div className="space-y-8 animate-fade-in-up">
            <div className="space-y-6">
              <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-cyan-100 to-sky-100 text-cyan-800 rounded-full text-sm font-medium shadow-sm hover:shadow-md transition-all duration-300 group">
                <Sparkles className="w-4 h-4 mr-2 animate-spin-slow" />
                <span className="group-hover:scale-105 transition-transform">Специализация: стоматология</span>
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight animate-fade-in-up delay-200">
                <span className="bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent">
                  {data.title}
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 leading-relaxed max-w-lg animate-fade-in-up delay-400">
                {data.subtitle}
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 animate-fade-in-up delay-600">
              <Button 
                onClick={onOpenForm}
                size="lg" 
                className="bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105 group relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
                <span className="relative">Получить консультацию</span>
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform relative" />
              </Button>
              
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="border-2 border-cyan-300 hover:border-cyan-500 hover:text-cyan-600 hover:bg-cyan-50 px-6 py-4 text-lg font-medium transition-all duration-300 hover:shadow-md hover:-translate-y-0.5"
                >
                  <Phone className="mr-2 h-5 w-5" />
                  Позвонить
                </Button>
                
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="border-2 border-cyan-300 hover:border-green-500 hover:text-green-600 hover:bg-green-50 px-6 py-4 text-lg font-medium transition-all duration-300 hover:shadow-md hover:-translate-y-0.5"
                >
                  <MessageCircle className="mr-2 h-5 w-5" />
                  WhatsApp
                </Button>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-8 animate-fade-in-up delay-800">
              {data.stats.map((stat, index) => (
                <div key={index} className="text-center group">
                  <div className="text-3xl font-bold bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent mb-1 group-hover:scale-110 transition-transform duration-300">
                    {stat.number}
                  </div>
                  <div className="text-sm text-gray-600 group-hover:text-cyan-600 transition-colors">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right content - Visual element */}
          <div className="relative animate-fade-in-right delay-400">
            <Card className="p-8 bg-white/80 backdrop-blur-sm shadow-2xl border-0 hover:shadow-3xl transition-all duration-500 hover:-translate-y-2 relative overflow-hidden group">
              {/* Card background animation */}
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-50/50 to-sky-100/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div className="space-y-6 relative z-10">
                <div className="text-center">
                  {/* Professional full-body photo */}
                  <div className="w-40 h-48 mx-auto mb-4 relative group/avatar overflow-hidden rounded-2xl shadow-lg group-hover/avatar:shadow-2xl transition-all duration-500">
                    <img 
                      src="https://static.tildacdn.com/tild3433-6665-4038-a139-336463353464/555_1.png"
                      alt="Екатерина Егорова - Специалист по контекстной рекламе"
                      className="w-full h-full object-cover transition-all duration-500 group-hover/avatar:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-cyan-600/20 via-transparent to-transparent opacity-0 group-hover/avatar:opacity-100 transition-opacity duration-500"></div>
                    
                    {/* Floating badge */}
                    <div className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full shadow-lg animate-pulse">
                      Online
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2 group-hover:text-cyan-700 transition-colors">
                    Екатерина Егорова
                  </h3>
                  <p className="text-gray-600 group-hover:text-cyan-600 transition-colors">
                    Специалист по контекстной рекламе для стоматологий
                  </p>
                </div>
                
                <div className="border-t pt-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group/item">
                      <span className="text-gray-700 group-hover/item:text-emerald-700 transition-colors">Средняя стоимость заявки</span>
                      <span className="font-bold text-green-600 group-hover/item:scale-110 transition-transform">от 350₽</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group/item">
                      <span className="text-gray-700 group-hover/item:text-cyan-700 transition-colors">Конверсия</span>
                      <span className="font-bold text-cyan-600 group-hover/item:scale-110 transition-transform">8-12%</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group/item">
                      <span className="text-gray-700 group-hover/item:text-purple-700 transition-colors">Срок запуска</span>
                      <span className="font-bold text-purple-600 group-hover/item:scale-110 transition-transform">3-5 дней</span>
                    </div>
                  </div>
                </div>

                {/* Trust indicator */}
                <div className="flex items-center justify-center space-x-2 text-cyan-600 bg-cyan-50 rounded-lg p-3 group-hover:bg-cyan-100 transition-colors">
                  <TrendingUp className="h-5 w-5 animate-bounce" />
                  <span className="font-semibold text-sm">Результат гарантирован!</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;