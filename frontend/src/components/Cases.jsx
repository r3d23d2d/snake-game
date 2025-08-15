import React, { useState } from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ArrowRight, TrendingUp, DollarSign, Users, Calendar, Award, Zap } from 'lucide-react';

const Cases = ({ data }) => {
  const [selectedCase, setSelectedCase] = useState(data[0]);

  return (
    <section id="cases" className="py-20 bg-gradient-to-br from-cyan-50 via-white to-sky-50 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-200/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-sky-300/15 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="text-center mb-16 animate-fade-in-up">
          <Badge className="bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 px-4 py-2 text-sm mb-4 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105">
            <Award className="w-4 h-4 mr-2" />
            Проверенные результаты
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-6">
            Реальные кейсы моих клиентов
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Каждый кейс — это история успеха стоматологической клиники, 
            которая получила стабильный поток новых пациентов
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Case selector */}
          <div className="lg:col-span-1 animate-fade-in-left">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Zap className="w-5 h-5 mr-2 text-cyan-600" />
                Выберите кейс:
              </h3>
              {data.map((caseItem, index) => (
                <Card 
                  key={caseItem.id}
                  className={`cursor-pointer transition-all duration-500 border-2 hover:shadow-xl hover:-translate-y-1 group ${
                    selectedCase.id === caseItem.id 
                      ? 'border-cyan-500 shadow-xl bg-gradient-to-br from-cyan-50 to-sky-50 scale-105' 
                      : 'border-gray-200 hover:border-cyan-300 hover:shadow-lg bg-white/80 backdrop-blur-sm'
                  }`}
                  onClick={() => setSelectedCase(caseItem)}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <CardContent className="p-4">
                    <h3 className={`font-bold mb-1 text-sm transition-colors duration-300 ${
                      selectedCase.id === caseItem.id ? 'text-cyan-700' : 'text-gray-900 group-hover:text-cyan-600'
                    }`}>
                      {caseItem.title}
                    </h3>
                    <p className="text-gray-600 text-xs mb-3">
                      {caseItem.subtitle}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-green-600 font-semibold text-xs group-hover:scale-105 transition-transform">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        {caseItem.results.growth}
                      </div>
                      <div className="text-cyan-600 text-xs font-medium">
                        {caseItem.results.leads} заявок
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Selected case details */}
          <div className="lg:col-span-2 animate-fade-in-right">
            <Card className="shadow-2xl border-0 overflow-hidden hover:shadow-3xl transition-all duration-500 bg-white/90 backdrop-blur-sm">
              <div className="bg-gradient-to-r from-cyan-600 to-sky-600 text-white p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
                <div className="absolute bottom-0 left-0 w-24 h-24 bg-cyan-400/20 rounded-full translate-y-12 -translate-x-12"></div>
                <div className="relative z-10">
                  <h3 className="text-3xl font-bold mb-2 animate-fade-in-up">{selectedCase.title}</h3>
                  <p className="text-cyan-100 text-lg mb-4 animate-fade-in-up delay-100">{selectedCase.subtitle}</p>
                  <p className="text-lg animate-fade-in-up delay-200">{selectedCase.description}</p>
                </div>
              </div>
              
              <CardContent className="p-8">
                {/* Results */}
                <div className="mb-8">
                  <h4 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                    <TrendingUp className="w-6 h-6 mr-2 text-cyan-600" />
                    Результаты работы
                  </h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 text-center hover:shadow-lg transition-all duration-300 hover:scale-105 group">
                      <Users className="h-8 w-8 text-green-600 mx-auto mb-3 group-hover:animate-bounce" />
                      <div className="text-3xl font-bold text-green-600 mb-1 group-hover:scale-110 transition-transform">
                        {selectedCase.results.leads}
                      </div>
                      <div className="text-gray-600">заявок в месяц</div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-cyan-50 to-sky-50 rounded-2xl p-6 text-center hover:shadow-lg transition-all duration-300 hover:scale-105 group">
                      <DollarSign className="h-8 w-8 text-cyan-600 mx-auto mb-3 group-hover:animate-bounce" />
                      <div className="text-3xl font-bold text-cyan-600 mb-1 group-hover:scale-110 transition-transform">
                        {selectedCase.results.cost_per_lead}₽
                      </div>
                      <div className="text-gray-600">стоимость заявки</div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-purple-50 to-violet-50 rounded-2xl p-6 text-center hover:shadow-lg transition-all duration-300 hover:scale-105 group">
                      <Calendar className="h-8 w-8 text-purple-600 mx-auto mb-3 group-hover:animate-bounce" />
                      <div className="text-3xl font-bold text-purple-600 mb-1 group-hover:scale-110 transition-transform">
                        {selectedCase.results.budget.toLocaleString()}₽
                      </div>
                      <div className="text-gray-600">бюджет в месяц</div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-2xl p-6 text-center hover:shadow-lg transition-all duration-300 hover:scale-105 group">
                      <TrendingUp className="h-8 w-8 text-orange-600 mx-auto mb-3 group-hover:animate-bounce" />
                      <div className="text-3xl font-bold text-orange-600 mb-1 group-hover:scale-110 transition-transform">
                        {selectedCase.results.growth}
                      </div>
                      <div className="text-gray-600 font-medium">рост пациентов</div>
                    </div>
                  </div>
                </div>

                {/* Process */}
                <div className="mb-8">
                  <h4 className="text-xl font-bold text-gray-900 mb-4">Что делали</h4>
                  <p className="text-gray-600 mb-6 text-lg leading-relaxed">{selectedCase.tasks}</p>
                  
                  <div className="space-y-3">
                    {selectedCase.process.map((step, index) => (
                      <div 
                        key={index} 
                        className="flex items-center p-4 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group"
                        style={{ animationDelay: `${index * 100}ms` }}
                      >
                        <div className="w-8 h-8 bg-gradient-to-br from-cyan-600 to-sky-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4 shadow-lg group-hover:scale-110 transition-transform">
                          {index + 1}
                        </div>
                        <span className="text-gray-800 group-hover:text-cyan-700 transition-colors font-medium">{step}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CTA */}
                <div className="bg-gradient-to-r from-cyan-50 to-sky-50 rounded-2xl p-8 text-center relative overflow-hidden group hover:shadow-lg transition-all duration-300">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-cyan-200/30 rounded-full -translate-y-10 translate-x-10 group-hover:scale-150 transition-transform duration-500"></div>
                  <div className="relative z-10">
                    <h5 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-cyan-700 transition-colors">
                      Хотите такие же результаты?
                    </h5>
                    <p className="text-gray-600 mb-4 text-lg">
                      Обсудим ваш проект и составим план продвижения
                    </p>
                    <Button className="bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white px-8 py-3 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group/btn relative overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover/btn:opacity-20 transition-opacity duration-300"></div>
                      <span className="relative">Получить консультацию</span>
                      <ArrowRight className="ml-2 h-5 w-5 group-hover/btn:translate-x-1 transition-transform relative" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Cases;