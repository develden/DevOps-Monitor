describe('DevOps Monitor UI Tests', () => {
  it('Отображает Дашборд сборок и фильтрацию', () => {
    cy.visit('/');
    cy.contains('Дашборд сборок');
    cy.get('input[label="Поиск сборок"]').should('exist');
  });

  it('Проверяет работу интерфейса управления сборками', () => {
    cy.visit('/build-manager');
    cy.contains('Управление сборками');
    cy.get('input').first().type('Test Job');
    cy.get('button').contains('Запустить сборку').click();
    // Проверка появления уведомления (Snackbar)
    cy.get('.MuiAlert-message').should('exist');
  });
}); 