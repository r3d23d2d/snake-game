import React, { useEffect, useRef } from 'react';
import { Card, CardContent } from './ui/card';
import { Search, Target, TrendingUp, PieChart, Clock, Zap } from 'lucide-react';

const iconMap = {
  Search,
  Target, 
  TrendingUp,
  PieChart
};

const Services = ({ data }) => {
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up');
          }
        });
      },
      { threshold: 0.1 }
    );

    const cards = sectionRef.current?.querySelectorAll('.service-card');
    cards?.forEach((card) => observer.observe(card));

    return () => observer.disconnect();
  }, []);

  return (
    <section id="services" className="py-20 bg-gradient-to-br from-white via-cyan-25 to-sky-50 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-10 right-10 w-64 h-64 bg-cyan-200/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-sky-300/15 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative" ref={sectionRef}>
        <div className="text-center mb-16 animate-fade-in-up">
          <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-cyan-100 to-sky-100 text-cyan-800 rounded-full text-sm font-medium mb-4 shadow-sm">
            <Zap className="w-4 h-4 mr-2 animate-pulse" />
            Проверенная методология
          </div>
          <h2 className="text-3xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-6">
            Как я работаю с вашей стоматологией
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Проверенная методология, которая приносит стабильные результаты 
            стоматологическим клиникам уже более 6 лет
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {data.map((service, index) => {
            const Icon = iconMap[service.icon];
            return (
              <Card 
                key={service.id} 
                className="service-card group hover:shadow-2xl transition-all duration-500 border-0 shadow-lg hover:-translate-y-3 relative overflow-hidden bg-white/80 backdrop-blur-sm"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                {/* Card glow effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/10 to-sky-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                
                <CardContent className="p-8 text-center relative z-10">
                  <div className="mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-cyan-100 to-sky-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-gradient-to-br group-hover:from-cyan-600 group-hover:to-sky-600 transition-all duration-500 shadow-lg group-hover:shadow-xl group-hover:scale-110">
                      <Icon className="h-8 w-8 text-cyan-600 group-hover:text-white transition-all duration-500 group-hover:scale-110" />
                    </div>
                    <div className="text-2xl font-bold text-cyan-600 mb-2 group-hover:scale-110 transition-transform duration-300">
                      0{index + 1}
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-4 group-hover:text-cyan-700 transition-colors duration-300">
                    {service.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed group-hover:text-gray-700 transition-colors duration-300">
                    {service.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Process timeline */}
        <div className="mt-20">
          <div className="text-center mb-12 animate-fade-in-up">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-4">
              Весь процесс займет всего 3-5 дней
            </h3>
            <p className="text-gray-600 flex items-center justify-center">
              <Clock className="w-5 h-5 mr-2 text-cyan-600" />
              От первого звонка до запуска рекламы
            </p>
          </div>
          
          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-cyan-300 to-sky-400 shadow-lg"></div>
            
            <div className="space-y-12">
              {[
                { day: "День 1", title: "Консультация и анализ", desc: "Изучаем вашу клинику, конкурентов и текущую ситуацию", color: "from-cyan-500 to-cyan-600" },
                { day: "День 2-3", title: "Стратегия и настройка", desc: "Создаем стратегию продвижения и настраиваем кампании", color: "from-sky-500 to-sky-600" },
                { day: "День 4-5", title: "Запуск и первые результаты", desc: "Запускаем рекламу и получаем первые заявки", color: "from-cyan-600 to-sky-600" }
              ].map((step, index) => {
                // День 2-3 (index 1) должен быть справа, остальные по стандартной логике  
                const isRight = index === 1 || (index !== 1 && index % 2 !== 0);
                return (
                <div key={index} className={`flex items-center ${isRight ? 'justify-end' : 'justify-start'} animate-fade-in-up`} style={{ animationDelay: `${index * 300}ms` }}>
                  <div className={`w-5/12 ${isRight ? 'pl-8 text-left' : 'pr-8 text-right'}`}>
                    <Card className="p-6 shadow-xl border-0 bg-white/90 backdrop-blur-sm hover:shadow-2xl transition-all duration-500 hover:-translate-y-1 group">
                      <div className="space-y-2">
                        <div className={`text-cyan-600 font-bold text-lg bg-gradient-to-r ${step.color} bg-clip-text text-transparent group-hover:scale-110 transition-transform`}>{step.day}</div>
                        <h4 className="font-bold text-gray-900 text-lg group-hover:text-cyan-700 transition-colors">{step.title}</h4>
                        <p className="text-gray-600 text-sm leading-relaxed">{step.desc}</p>
                      </div>
                    </Card>
                  </div>
                  
                  <div className={`w-10 h-10 bg-gradient-to-br ${step.color} rounded-full border-4 border-white shadow-xl z-10 flex items-center justify-center hover:scale-125 transition-transform duration-300 cursor-pointer`}>
                    <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                  </div>
                  
                  <div className="w-5/12"></div>
                </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Services;