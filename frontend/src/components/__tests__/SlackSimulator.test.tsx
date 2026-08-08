import { render, screen } from '@testing-library/react'
import SlackSimulator from '../SlackSimulator'

test('renders textarea', ()=>{
  render(<SlackSimulator incidentId={1} />)
  expect(screen.getByRole('textbox')).toBeTruthy()
})
